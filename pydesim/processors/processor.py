import abc
from typing import Any, Optional

import pydantic as da
import typing_extensions as te

from .. import constants as const
from ..content import Content


class Processor(abc.ABC):
    next_event_time: da.NonNegativeFloat
    last_event_time: da.NonNegativeFloat

    def __init__(
        self,
        name: str,
        in_ports: dict = da.Field({}),
        out_ports: dict = da.Field({}),
    ) -> None:
        self.next_event_time = const.INF
        self.last_event_time = const.INF
        self.name = name
        self.in_ports = in_ports if in_ports else {}
        self.out_ports = out_ports if out_ports else {}

    @abc.abstractmethod
    def initialize(self, current_time: float):
        """Should set `next_event_time`"""
        self.time_advance()

    def int_transition(self, time: float) -> Any:
        raise NotImplementedError()

    def ext_transition(self, content: Content, time: float) -> None:
        raise NotImplementedError()

    def time_advance(self):
        raise NotImplementedError()

    def find(self, name: str) -> Optional[None]:
        """
        iteratively searchs entity with given name
        from the children tree
        """
        raise NotImplemented

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self) -> str:
        return f"Model({self.name})"
