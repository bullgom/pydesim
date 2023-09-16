import abc

from ... import port as po
from . import processor as pr
from . import selector


class _BaseParent(pr.Processor):
    _children: list[pr.Processor]

    def __init__(self) -> None:
        super().__init__()
        self._children = []

    @abc.abstractmethod
    def done(self, source: pr.Processor, t: float) -> None:
        raise NotImplementedError

    def initialize(self) -> float:
        for child in self._children:
            child.initialize()
        return self._next_event_time

    @abc.abstractmethod
    def y(self, t: float, port: list[po.Port]) -> None:
        raise NotImplementedError
