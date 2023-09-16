import abc

from ... import port as po
from . import base_parent, child, selector
from . import processor as pr


class Parent(base_parent._BaseParent):
    _children: list[child.Child]
    _imminent_children: list[child.Child]
    _selector: selector.Selector

    def __init__(self, selector: selector.Selector = selector.FIFO()) -> None:
        super().__init__()
        self._selector = selector
        self._imminent_children = []

    def done(self, source: child.Child, t: float) -> None:
        if t < self._next_event_time:
            self._imminent_children.clear()
            self._imminent_children.append(source)
            self._next_event_time = t

    def adopt(self, *child: child.Child) -> None:
        self._children.extend(child)

    @abc.abstractmethod
    def y(self, t: float, ports: list[po.Port]) -> None:
        raise NotImplementedError
