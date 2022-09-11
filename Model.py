from . import INF, NEG_INF, Content
from .port_manager import PortManager
from .Content import Content

class Model:

    def __init__(
            self,
            name,
            parent=None,
            cell_pos=None,
            in_ports={},
            out_ports={},
            next_event_time=INF,
            last_event_time=NEG_INF):

        self.name = name
        self.parent = parent
        self.in_ports = PortManager(in_ports)
        self.out_ports = PortManager(out_ports)
        self.cell_pos = cell_pos
        self.next_event_time = next_event_time
        self.last_event_time = last_event_time

        if self.parent:
            if self not in self.parent.children:
                self.parent.children.append(self)

    def initialize(self):
        raise NotImplementedError()

    def int_transition(self, time:float):
        raise NotImplementedError()

    def ext_transition(self, content:Content, time:float):
        raise NotImplementedError()

    def time_advance(self):
        raise NotImplementedError()

    def __eq__(self, other):
        return self.name == other.name
