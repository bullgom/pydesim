from .. import port as po
from . import base_model as bm
from . import port as mp
from .. import project_types as pt
from .. import constants as const

PairedPortDict = dict[str, mp.PairedPort]


class Model(bm.BaseModel):
    def __init__(self, in_ports: po.PortDict, out_ports: po.PortDict) -> None:
        super().__init__()
        self.in_ports: PairedPortDict = {k: mp.PairedPort(self) for k in in_ports}
        self.out_ports: PairedPortDict = {k: mp.PairedPort(self) for k in out_ports}

    def hold(self, state_duration: pt.VirtualTime = const.INF) -> None:
        self.time_until_event = state_duration

    def resume(self, elapsed_time: pt.VirtualTime):
        self.time_until_event = self.time_until_event - elapsed_time

    def advance_time(self, current_time: pt.VirtualTime) -> pt.VirtualTime:
        """
        Advances the next time of event and returns it.
        For internal use by Processors
        """
        next_event_time = current_time + self.time_until_event
        return next_event_time

    @property
    def time_until_event(self) -> pt.VirtualTime:
        return self.state.time_until_event

    @time_until_event.setter
    def time_until_event(self, value: pt.VirtualTime) -> None:
        self.state.time_until_event = value
