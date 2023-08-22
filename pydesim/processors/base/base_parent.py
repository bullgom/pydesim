import abc

from ... import port as po
from . import processor as pr
from . import selector


class _BaseParent(pr.Processor):
    _children: list[pr.Processor]
    _imminent: list[pr.Processor]
    _selector: selector.Selector

    def __init__(self, selector: selector.Selector = selector.FIFO()) -> None:
        self._imminent = []
        self._selector = selector

    def done(self, source: pr.Processor, t: float) -> None:
        if t < self._next_event_time:
            self._imminent.clear()
            self._imminent.append(source)
            self._next_event_time = t

    def initialize(self) -> float:
        for child in self._children:
            child.initialize()
        return self._next_event_time

    @abc.abstractmethod
    def y(self, t: float, port: list[po.Port]) -> None:
        raise NotImplementedError
