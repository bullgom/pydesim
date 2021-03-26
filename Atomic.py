from pydesim import INF, NEG_INF, PASSIVE, Message, Model, PortManager
from functools import wraps
from typing import Optional
import math
import numpy as np


class Atomic(Model):

    def __init__(
            self,
            name: str,
            parent: Optional[Model]=None,
            cell_pos=None,
            in_ports:Optional[dict]={},
            out_ports:Optional[dict]={},
            next_event_time:Optional[float]=INF,
            last_event_time:Optional[float]=NEG_INF,
            elapsed_time:Optional[float]=INF,
            state=PASSIVE,
            sigma:Optional[float]=INF,
            ext_transition_callbacks:Optional[list]=[],
            int_transition_callbacks:Optional[list]=[]):
        super().__init__(
            name,
            parent,
            cell_pos,
            in_ports,
            out_ports,
            next_event_time,
            last_event_time)

        self.elapsed_time = elapsed_time
        self.state = state
        self.sigma = sigma
        self.int_transition_callbacks = int_transition_callbacks
        self.ext_transition_callbacks = ext_transition_callbacks
        self.initial_state = {
            "state": self.state,
            "sigma": self.sigma,
            "cell_pos": self.cell_pos,
            "next_event_time": self.next_event_time,
            "last_event_time": self.last_event_time,
            "elapsed_time": self.elapsed_time
        }

    def initialize(self):
        self.state = self.initial_state["state"]
        self.sigma = self.initial_state["sigma"]
        self.cell_pos = self.initial_state["cell_pos"]
        self.next_event_time = self.initial_state["next_event_time"]
        self.last_event_time = self.initial_state["last_event_time"]
        self.elapsed_time = self.initial_state["elapsed_time"]

    def hold_in(self, state:str, sigma:Optional[float] = INF):
        self.state = state
        self.sigma = sigma

    def resume(self):
        if math.isfinite(self.sigma):
            self.sigma -= self.elapsed_time

    def time_advance(self, time:float):
        self.last_event_time = time
        self.next_event_time = time + self.sigma

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
