from . import Model, Message, Content, INF, NEG_INF, Atomic, Port
from typing import Optional

class Digraph(Model):

    def __init__(
            self,
            *args,
            int_couplings : dict | None = None,
            ext_output_couplings : dict | None = None,
            ext_input_couplings : dict | None = None,
            **kwargs
        ):
        super().__init__(*args, **kwargs)

        self.next_event_models = []
        self.children = []
        self.int_couplings = int_couplings if int_couplings else {}
        self.ext_output_couplings = ext_output_couplings if ext_output_couplings else {}
        self.ext_input_couplings = ext_input_couplings if ext_input_couplings else {}

    def couple(self, source_port: Port, target_port: Port):
        assert type(source_port) is Port and type(target_port) is Port

        coupling = None

        if source_port.model is self and target_port.model in self.children:
            coupling = self.ext_input_couplings
        elif source_port.model in self.children and target_port.model is self:
            coupling = self.ext_output_couplings
        elif source_port.model in self.children and target_port.model in self.children:
            coupling = self.int_couplings
        else:
            raise ValueError("Wrong coupling")

        try:
            if target_port not in coupling[source_port]:
                coupling[source_port].append(target_port)
        except KeyError:
            coupling[source_port] = [target_port]

    def int_transition(self, time: float):
        result = []
        for child in self.next_event_models:
            output = child.int_transition(time)
            if output:
                result += output
            else:
                break

        to_parent = []
        parent_append = to_parent.append
        int_couplings = self.int_couplings
        ext_output_couplings = self.ext_output_couplings

        for message in result:
            src = message.source
            value = message.content.value
            if message.content.port in int_couplings:
                for target_port in int_couplings[message.content.port]:
                    target_port.model.ext_transition(
                        Message(src, time, Content(target_port, value)))
            if message.content.port in ext_output_couplings:
                for target_port in ext_output_couplings[message.content.port]:
                    parent_append(
                        Message(src, time, Content(target_port, value)))

        self.time_advance()
        return to_parent

    def ext_transition(self, message: Message):

        src = message.source
        time = message.time
        value = message.content.value
        for target_port in self.ext_input_couplings[message.content.port]:
            target_port.model.ext_transition(
                Message(src, time, Content(target_port, value)))
        self.time_advance()

    def time_advance(self):
        self.last_event_time = self.next_event_time

        min_time = min(self.children, key=lambda x: x.next_event_time)
        self.next_event_models = [m for m in self.children if m.next_event_time == min_time]

        self.next_event_time = min_time

    def initialize(self):
        for child in self.children:
            child.initialize()
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

    def find(self, name: str):
        """
        iteratively looks for entity with given name
        from all children tree
        """

        for child in self.children:
            if child.name == name:
                return child
            elif issubclass(type(child), Digraph):
                temp = child.find(name)
                if temp:
                    return temp
        return None
