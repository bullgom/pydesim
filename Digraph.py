from model import Model
from message import Message
from constants import INF, NEG_INF
from port import Port

class Digraph(Model):

    def __init__(
            self,
            *args,
            int_couplings : dict | None = None,
            ext_output_couplings : dict | None = None,
            ext_input_couplings : dict | None = None,
            ta_function: str = "unnested",
            **kwargs
        ):
        super().__init__(*args, **kwargs)

        self.next_event_models : list[Model] = []
        self.children : list[Model] = []
        self.int_couplings : dict[Port, list[Port]] =  \
            int_couplings if int_couplings else {}
        self.ext_output_couplings : dict[Port, list[Port]] = \
            ext_output_couplings if ext_output_couplings else {}
        self.ext_input_couplings : dict[Port, list[Port]] = \
            ext_input_couplings if ext_input_couplings else {}
        
        if ta_function == "unnested":
            self._time_advance = self.time_advance_unnested
        elif ta_function == "nested":
            self._time_advance = self.time_advance_nested
        else:
            raise ValueError(f"{ta_function} is not allowed")

    def couple(self, source_port: Port, target_port: Port):
        """Couples two ports with direction"""
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

        to_parent = []
        for message in result:
            if message.content.port in self.int_couplings:
                self.on_int(message)
                    
            if message.content.port in self.ext_output_couplings:
                to_parent += self.on_ext_output(message)

        self.time_advance()
        return to_parent

    def on_int(self, message: Message) -> None:
        for target_port in self.int_couplings[message.content.port]:
            target_port.model.ext_transition(message.translate(target_port))
        return None

    def on_ext_output(self, message: Message) -> list[Message]:
        to_parent = []
        for target_port in self.ext_output_couplings[message.content.port]:
            to_parent.append(message.translate(target_port))
        return to_parent

    def ext_transition(self, message: Message):
        target_ports = self.ext_input_couplings[message.content.port]
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
        self.next_event_models = [m for m in self.children if m.next_event_time == min_time]

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

    def find(self, name: str) -> Model | None:
        if self.name == name:
            return self
        
        for child in self.children:
            res = child.find(child)
            if res:
                return res

        return None
