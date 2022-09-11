from . import INF, NEG_INF, PASSIVE, Message, Model
from functools import wraps
from typing import Optional, Callable
import math


class Atomic(Model):

    def __init__(
            self,
            *args,
            ext_transition_callbacks: list[Callable] | None = None,
            int_transition_callbacks: list[Callable] | None = None,
            **kwargs
        ):
        super().__init__(*args, **kwargs)

        self.elapsed_time = INF
        self.state = PASSIVE
        self.time_until_event = INF
        self.int_transition_callbacks = int_transition_callbacks \
            if int_transition_callbacks else []
        self.ext_transition_callbacks = ext_transition_callbacks \
            if ext_transition_callbacks else []

    def hold_in(self, state:str, sigma:Optional[float] = INF):
        self.state = state
        self.time_until_event = sigma

    def resume(self):
        if math.isfinite(self.time_until_event):
            self.time_until_event -= self.elapsed_time

    def time_advance(self, time:float):
        self.last_event_time = time
        self.next_event_time = time + self.time_until_event

    def find(self, name: str) -> "Model" | None:
        return self if name == self.name else None
        
        

    @staticmethod
    def int_transition_wrapper(int_transition):
        @wraps(int_transition)
        def wrapper(self, *args, **kwargs):
            self.elapsed_time = args[0]-self.last_event_time
            result = int_transition(self, *args, **kwargs)
            self.time_advance(args[0])
            for callback in self.int_transition_callbacks:
                callback(self, args, result)
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
            self.elapsed_time = args[0].time-self.last_event_time
            ext_transition(self, args[0].content, args[0].time)
            self.time_advance(args[0].time)
            for callback in self.ext_transition_callbacks:
                callback(self, args[0])
        return wrapper
