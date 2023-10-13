import abc
import typing as ty
from . import project_types as pt
from . import port as po
from . import constants as const


class Model(abc.ABC):
    state: pt.State

    def __init__(self, in_ports: po.PortDict, out_ports: po.PortDict) -> None:
        self.in_ports: po.PortDict = in_ports
        self.out_ports: po.PortDict = out_ports

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
    def external_transition(self, elapsed_time: pt.VirtualTime, ports: list[po.Port]):
        """Should implement the external transition funciton."""
        raise NotImplementedError

    def hold(self, state_duration: pt.VirtualTime = const.INF) -> None:
        self.time_until_event = state_duration

    def resume(self, elapsed_time: pt.VirtualTime):
        self.time_until_event = self.time_until_event - elapsed_time

    def _call_initialize(self) -> None:
        """For internal use."""
        self.initialize()
        if not hasattr(self, "state"):
            ValueError(
                f"State not initialized. Is the initial state set in the initialize function?"
            )

    def _advance_time(self, current_time: pt.VirtualTime) -> pt.VirtualTime:
        """
        Advances the next time of event and returns it.
        For internal use by Processors
        """
        next_event_time = current_time + self.time_until_event
        self.time_until_event = next_event_time
        return next_event_time

    @property
    def time_until_event(self) -> pt.VirtualTime:
        return self.state.time_until_event

    @time_until_event.setter
    def time_until_event(self, value: pt.VirtualTime) -> None:
        self.state.time_until_event = value
