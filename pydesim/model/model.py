import abc
import typing as ty

from .. import constants as const
from .. import port as po
from . import state as st


class Model(abc.ABC):
    _name: str
    _remaining_time: float
    _state: st.State
    _in_ports: list[po.Port]
    _out_ports: list[po.Port]

    def __init__(self, name: str):
        self._name = name
        self._in_ports = list()
        self._out_ports = list()
        self._remaining_time = const.INF

    def hold_for(self, duration: float) -> None:
        self._remaining_time = duration

    def hold_in(self, state: st.State, duration: float) -> None:
        self._state = state
        self._remaining_time = duration

    def resume(self, elapsed_time: float) -> None:
        self._remaining_time -= elapsed_time

    def ta(self) -> float:
        """Time advance function. Returns how much the model consumed."""
        return self._remaining_time

    @abc.abstractmethod
    def initialize(self) -> float:
        ...

    @abc.abstractmethod
    def internal(self, current_time: float) -> ty.Any:
        raise NotImplementedError()

    @abc.abstractmethod
    def external(self, elapsed_time: float, port: po.Port) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def output(self) -> list[po.Port]:
        """The output function. y <- output(s)"""
        return self._out_ports

    def __repr__(self) -> str:
        return f"Model({self._name})"
