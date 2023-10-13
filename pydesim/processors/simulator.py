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
class Simulator(Processor):
    state: Any
    time_until_event: float

    def __init__(self, in_ports: po.PortDict, out_ports: po.PortDict):
        super().__init__(in_ports, out_ports)

        self.time_until_event = INF

    def hold_in(self, state: Any, sigma: float = INF):
        self.state = state
        self.time_until_event = sigma

    def resume(self):
        if math.isfinite(self.time_until_event):
            self.time_until_event -= self.elapsed_time

    def time_advance(self, current_time: pt.VirtualTime):
        self.last_event_time = current_time
        self.next_event_time = current_time + self.time_until_event

    @abc.abstractmethod
    def internal_transition(self, )

    @staticmethod
    def int_transition_wrapper(int_transition: Callable):
        @wraps(int_transition)
        def wrapper(self: Self, *args, **kwargs):
            elapsed_time = args[0] - self.last_event_time
            result = int_transition(self, *args, **kwargs)
            self.time_advance(args[0])
                
            if result is None:
                return None
            elif type(result) is not list:
                return [Message(self.name, args[0], result)]
            else:
                return [Message(self.name, args[0], y) for y in result]

        return wrapper

    @staticmethod
    def ext_transition_wrapper(ext_transition):
        @wraps(ext_transition)
        def wrapper(self, *args, **kwargs):
            self.elapsed_time = args[0].time - self.last_event_time
            ext_transition(self, args[0].content, args[0].time)
            self.time_advance(args[0].time)
            for callback in self.ext_transition_callbacks:
                callback(self, args[0])

        return wrapper
