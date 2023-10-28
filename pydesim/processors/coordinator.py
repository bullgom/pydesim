from ..models import port as po
from . import processor as pr
from .. import models as mo
from .. import project_types as pt
import typing as ty


class Coordinator(pr.Processor[mo.CoupledModel]):
    def __init__(
        self, model: mo.CoupledModel, processor_map: dict[mo.BaseModel, pr.Processor]
    ):
        super().__init__(model)

        self.processor_map: dict[mo.BaseModel, pr.Processor] = processor_map

    def internal_transition(self, current_time: pt.VirtualTime) -> list[po.PairedPort]:
        """On(*,from,t)
        send(*,self,t) to i*, where
            i* = select(imminent_children)
            imminent_children = {i in D | M_i.t_N = t}
        active_children <- active_children + {i*}
        """
        elapsed = self.elapsed_time(current_time)

        active_ports: list[po.PairedPort] = []
        for child in self.imminent_processors():
            active_ports += child.internal_transition(current_time)

        """On(y,from.t)
        for i in I[from] - {self}:
            send(Z_(from,i)(y),from,t) to i
            active_children <- active_children + {i}
        if self in I[from]:
            send(Z[from,self](y),self,t) to parent
        """
        to_parent: list[po.PairedPort] = []
        for port in active_ports:
            for target in self.model.internal_couplings.propagate(port):
                target.model.external_transition(elapsed, target)

            to_parent += self.model.out_couplings.propagate(port)

        self.advance_time(current_time)
        return to_parent

    def external_transition(
        self, current_time: pt.VirtualTime, active_port: po.PairedPort
    ) -> None:
        """On(x,from,t)
        for i in I_self:
            send(Z_(self,i)(x),self,t) to i
            active_children <- active_children + {i}
        """
        elapsed = self.elapsed_time(current_time)
        for port in self.model.in_couplings.propagate(active_port):
            port.model.external_transition(elapsed, port)
        self.advance_time(current_time)

    def imminent_processors(self) -> ty.Generator[pr.Processor, None, None]:
        for child in self.children():
            if child.next_event_time == self.next_event_time:
                yield child

    def children(self):
        return self.processor_map.values()

    def advance_time(self, current_time: pt.VirtualTime) -> None:
        super().advance_time(current_time)
        self.next_event_time = min(
            processor.next_event_time for processor in self.processor_map.values()
        )
