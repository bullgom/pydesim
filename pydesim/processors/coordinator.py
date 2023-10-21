from pydesim import project_types as pt
from pydesim.models import port as po
from ..models import port as po
from . import processor as pr
from .. import models as mo
from .. import project_types as pt


class Coordinator(pr.Processor[mo.CoupledModel]):
    def __init__(self, model: mo.CoupledModel):
        super().__init__(model)

        self.imminent_processors: list[pr.Processor] = []
        self.children: list[pr.Processor] = []

    def internal_transition(self, current_time: pt.VirtualTime) -> list[po.PairedPort]:
        elapsed = self.elapsed_time(current_time)

        active_ports: list[po.PairedPort] = []
        for child in self.imminent_processors:
            active_ports += child.internal_transition(current_time)

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
        elapsed = self.elapsed_time(current_time)
        for port in self.model.in_couplings.propagate(active_port):
            port.model.external_transition(elapsed, port)
        self.advance_time(current_time)

    def initialize(self, start_time: float = 0):
        for child in self.children:
            child.initialize(start_time)
        self.time_advance()
