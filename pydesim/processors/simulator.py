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
from ..models import model as mo


class Simulator(Processor[mo.Model]):
    def __init__(self, model: mo.Model):
        super().__init__(model)

    def internal_transition(self, current_time: pt.VirtualTime) -> list[po.Port]:
        results = self.model.internal_transition(current_time)
        self.advance_time(current_time)
        return results

    def external_transition(self, current_time: pt.VirtualTime, active_port: po.Port):
        elapsed = self.elapsed_time(current_time)
        self.model.external_transition(elapsed, active_port)
        self.advance_time(current_time)
