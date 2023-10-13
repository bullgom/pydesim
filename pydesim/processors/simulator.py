import math
from functools import wraps
from typing import Any, Callable, Optional

from typing_extensions import Self

from ..constants import INF, NEG_INF, PASSIVE
from ..message import Message
from .processor import Processor
import pydantic as da
from .. import port as po
from .. import project_types as pt
import abc
from .. import model as mo

class Simulator(Processor):

    def __init__(self, model: mo.Model):
        super().__init__(model)
        self.last_event_time: pt.VirtualTime = NEG_INF
    

    def internal_transition(self, current_time: pt.VirtualTime) -> list[po.Port]:
        results = self.__model.internal_transition(current_time)
        self.__model._advance_time(current_time)
        return results

    def external_transition(self, current_time: pt.VirtualTime, active_ports: list[po.Port]):
        elapsed = current_time - self.last_event_time
        self.__model.external_transition(elapsed, active_ports)
        self.__model._advance_time(current_time)
