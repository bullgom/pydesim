from .constants import INF, NEG_INF
from .processors.coordinator import Coordinator


class Simulation(Coordinator):
    def __init__(self, *args, time_limit=INF, **kwargs):
        super().__init__(*args, **kwargs)

        self.time_limit = time_limit

    def start(self):
        while self.next_event_time <= self.time_limit and self.next_event_time != INF:
            self.int_transition(self.next_event_time)
            self.time_advance()
