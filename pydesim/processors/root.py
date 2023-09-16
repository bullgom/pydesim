from pydesim import port as po
from pydesim.processors.base import child

from .. import model as mo
from . import base
from . import coordinator as co
from .. import constants as const


class RootCoordinator(base.Parent):
    _children: list[co.Coordinator]

    def run(self, max_time: float) -> None:
        """Execute simulation until given time or next_event_time is INF."""
        self.initialize()

        while self._running(self._next_event_time, max_time):
            self.coordinator.star(self._next_event_time)

    def adopt(self, child: co.Coordinator) -> None:
        if len(self._children):
            raise ValueError(f"{self.__class__.__name__} can only have one child.")
        return super().adopt(child)

    @staticmethod
    def _running(next_event_time: float, max_time: float) -> bool:
        return (next_event_time != const.INF) and (next_event_time <= max_time)

    @property
    def coordinator(self) -> co.Coordinator:
        return self._children[0]

    def y(self, t: float, port: list[po.Port]) -> None:
        ...