from ..constants import INF, NEG_INF
from ..message import Message
from .. import port as po
from . import processor as pr
from ..models import model as mo


class Coordinator(pr.Processor):
    def __init__(self, model: mo.Model, ta_function: str = "unnested"):
        super().__init__(model)

        self.next_event_models: list[pr.Processor] = []
        self.children: list[pr.Processor] = []

    def int_transition(self, time: float):
        result = []
        for child in self.next_event_models:
            output = child.int_transition(time)
            if output:
                result += output

        to_parent = []
        for message in result:
            if message.content.port in self.internal_couplings:
                self.on_int(message)

            if message.content.port in self.out_couplings:
                to_parent += self.on_ext_output(message)

        self.time_advance()
        return to_parent

    def add_children(self, *child: Processor) -> None:
        self.children += child

    def on_int(self, message: Message) -> None:
        for target_port in self.internal_couplings[message.content.port]:
            target_port.model.ext_transition(message.translate(target_port))
        return None

    def on_ext_output(self, message: Message) -> list[Message]:
        to_parent = []
        for target_port in self.out_couplings[message.content.port]:
            to_parent.append(message.translate(target_port))
        return to_parent

    def ext_transition(self, message: Message):
        target_ports = self.in_couplings[message.content.port]
        for target_port in target_ports:
            target_port.model.ext_transition(message.translate(target_port))
        self.time_advance()

    def time_advance(self):
        self.last_event_time = self.next_event_time
        self.next_event_time = self._time_advance()

    def time_advance_nested(self) -> float:
        """
        Use when duplicates are minimal
        """
        minval = float("inf")
        mins = []
        for child in self.children:
            if child.next_event_time < minval:
                minval = child.next_event_time
                mins = [child]
            elif child.next_event_time == minval:
                mins.append(child)

        return minval

    def time_advance_unnested(self) -> float:
        """
        Use when duplicates are common
        """
        min_time = min([m.next_event_time for m in self.children])
        self.next_event_models = [
            m for m in self.children if m.next_event_time == min_time
        ]

        return min_time

    def initialize(self, start_time: float = 0):
        for child in self.children:
            child.initialize(start_time)
        self.time_advance()

    def __getitem__(self, idx):
        return self.children[idx]

    def __iter__(self):
        self._iter_count = 0
        return self

    def __next__(self):
        x = self._iter_count
        self._iter_count += 1
        if x < len(self.children):
            return self.children[x]
        else:
            raise StopIteration

    def find(self, name: str) -> Processor | None:
        if self.name == name:
            return self

        for child in self.children:
            res = child.find(child)
            if res:
                return res

        return None
