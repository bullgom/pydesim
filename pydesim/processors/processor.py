import abc

import pydantic as da
import typing_extensions as te
import typing as ty
from .. import constants as const
from ..models import port as po
from ..models import model as mo
from .. import project_types as pt

M = ty.TypeVar("M", bound=mo.Model)


class Processor(abc.ABC, ty.Generic[M]):
    def __init__(self, model: M) -> None:
        self.next_event_time: da.NonNegativeFloat = const.INF
        self.last_event_time: da.NonNegativeFloat = 0
        self.model: M = model

    @abc.abstractmethod
    def internal_transition(self, current_time: pt.VirtualTime) -> list[po.PairedPort]:
        raise NotImplementedError

    @abc.abstractmethod
    def external_transition(
        self, current_time: pt.VirtualTime, active_port: po.PairedPort
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def advance_time(self, current_time: pt.VirtualTime) -> None:
        """Updates `next_event_time` and `last_event_time`.
        Subclasses must call `super().advance_time(current_time)`.
        """
        self.last_event_time = current_time

    def elapsed_time(self, current_time: pt.VirtualTime) -> pt.VirtualTime:
        return current_time - self.last_event_time
