import abc
import typing as ty
from . import project_types as pt
from . import port as po


class Model(abc.ABC):
    __states : list[pt.State]
    
    @abc.abstractmethod
    def initialize(self) -> None:
        """
        Should initialize its state
        Example:
        self.counter = State[int].initialize()
        """
        raise NotImplementedError

    @abc.abstractmethod
    def internal_transition(self, current_time: pt.VirtualTime) -> list[po.Port]:
        """Should implement the internal transition funciton."""
        raise NotImplementedError

    @abc.abstractmethod
    def external_transition(self, elapsed_time: pt.VirtualTime, ports: list[po.Port]):
        """Should implement the external transition funciton."""
        raise NotImplementedError

    def __setattr__(self, __name: str, __value: ty.Any) -> None:
        super().__setattr__(__name, __value)
        if isinstance(__value, pt.State):
            self.__states.append(__value)