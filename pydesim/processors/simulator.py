from pydesim import project_types as pt
from .processor import Processor
from .. import port as po
from .. import project_types as pt
from ..models import model as mo


class Simulator(Processor[mo.Model]):
    def __init__(self, model: mo.Model):
        super().__init__(model)

    def internal_transition(self, current_time: pt.VirtualTime) -> list[po.Port]:
        results = self.model.internal_transition(current_time)
        self.advance_time(current_time)
        return results

    def external_transition(self, current_time: pt.VirtualTime, active_port: po.Port):
        elapsed = self.elapsed_time(current_time)
        self.model.external_transition(elapsed, active_port)
        self.advance_time(current_time)

    def advance_time(self, current_time: pt.VirtualTime) -> None:
        super().advance_time(current_time)
        self.next_event_time = self.model.advance_time(current_time)
