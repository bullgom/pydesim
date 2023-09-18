from typing import Any, Optional

import pydantic as da
import typing_extensions as te

from ..constants import INF, NEG_INF
from ..content import Content


class Processor:
    def __init__(
        self,
        name: str,
        in_ports: dict = da.Field({}),
        out_ports: dict = da.Field({}),
        next_event_time: da.PositiveFloat = INF,
        last_event_time: da.PositiveFloat = NEG_INF,
    ) -> None:
        self.name = name
        self.in_ports = in_ports if in_ports else {}
        self.out_ports = out_ports if out_ports else {}
        self.next_event_time = next_event_time
        self.last_event_time = last_event_time

    def initialize(self):
        raise NotImplementedError()

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
