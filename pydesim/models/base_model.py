import abc
import typing as ty
from .. import project_types as pt
from .. import port as po
from .. import constants as const

class BaseModel(abc.ABC):
    state: pt.State

    @abc.abstractmethod
    def initialize(self) -> None:
        """
        Should initialize its state
        Example:
        self.state = StateSubclass(time_until_event=INF, other_state=1)
        """
        raise NotImplementedError

    @abc.abstractmethod
    def internal_transition(self, current_time: pt.VirtualTime) -> list[po.Port]:
        """Should implement the internal transition funciton."""
        raise NotImplementedError

    @abc.abstractmethod
    def external_transition(self, elapsed_time: pt.VirtualTime, active_port: po.Port):
        """Should implement the external transition funciton."""
        raise NotImplementedError


    def _initialize_implementation(self) -> None:
        """For internal use."""
        self.initialize()
        if not hasattr(self, "state"):
            ValueError(
                f"State not initialized. Is the initial state set in the initialize function?"
            )
