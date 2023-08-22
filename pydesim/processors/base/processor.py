import typing as ty
import abc
from ... import constants as const


class Processor(abc.ABC):
    _next_event_time: float
    _last_event_time: float

    def __init__(self) -> None:
        super().__init__()
        self._next_event_time = const.INF
        self._last_event_time = const.NINF

    @abc.abstractmethod
    def initialize(self) -> float:
        """Initialize and return next_event_time."""
        raise NotImplementedError