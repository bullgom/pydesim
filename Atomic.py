from desim import INF, NEG_INF, PASSIVE, Message, Model, PortManager
from functools import wraps


class Atomic(Model):

    def __init__(
            self,
            name,
            parent=None,
            in_ports=[],
            out_ports=[],
            cell_pos=None,
            next_event_time=INF,
            last_event_time=NEG_INF,
            elapsed_time=INF,
            state=PASSIVE,
            sigma=INF,
            ext_transition_callbacks=[],
            int_transition_callbacks=[]):
        super().__init__(
            name,
            parent,
            PortManager(in_ports),
            PortManager(out_ports),
            cell_pos,
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
        self.cell_pos = self.initial_state["cell"]
        self.next_event_time = self.initial_state["next_event_time"]
        self.last_event_time = self.initial_state["last_event_time"]
        self.elapsed_time = self.initial_state["elapsed_time"]

    def hold_in(self, state, sigma):
        self.state = state
        self.sigma = sigma

    def resume(self):
        """
        Arguments:
            time {[float]} -- [current time]
        """
        self.sigma -= self.elapsed_time

    def time_advance(self, time):
        self.last_event_time = time
        self.next_event_time = time + self.sigma

    def int_transition_wrapper(int_transition):
        @wraps(int_transition)
        def wrapper(self, *args, **kwargs):
            result = int_transition(self, *args, **kwargs)
            self.time_advance(kwargs['time'])
            for callback in self.int_transition_callbacks:
                callback(self)
            if result is None:
                return None
            elif type(result) is not list:
                return [Message(self, kwargs['time'], result)]
            else:
                return [Message(self, kwargs['time'], y) for y in result]
        return wrapper

    def ext_transition_wrapper(ext_transition):
        @wraps(ext_transition)
        def wrapper(self, *args, **kwargs):
            self.elapsed_time = kwargs['message'].time-self.last_event_time
            ext_transition(self, kwargs['message'].content)
            self.time_advance(kwargs['time'])
            for callback in self.ext_transition_callbacks:
                callback(self)
