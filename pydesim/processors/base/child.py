import abc
import typing as ty

from ... import model as mo
from ... import port as po
from . import base_parent, has_model
from . import processor as pr

_M = ty.TypeVar("_M", bound=mo.Model)


class Child(pr.Processor, has_model.HasModel[_M], ty.Generic[_M]):
    _parent: base_parent._BaseParent

    def __init__(self, model: _M, parent: base_parent._BaseParent) -> None:
        pr.Processor.__init__(self)
        has_model.HasModel[_M].__init__(self, model)
        self._parent = parent

    def initialize(self) -> float:
        self._parent.done(self, self._next_event_time)
        return self._next_event_time

    @abc.abstractmethod
    def star(self, current_time: float) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def x(self, t: float, port: po.Port) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def y(self, t: float, ports: list[po.Port]) -> None:
        raise NotImplementedError
