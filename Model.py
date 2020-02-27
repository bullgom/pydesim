from desim import PortManager, INF, NEG_INF


class Model:

    def __init__(
        self,
        name,
        parent=None,
        in_ports=PortManager(),
        out_ports=PortManager(),
        cell_pos=None,
        next_event_time=INF,
        last_event_time=NEG_INF):

        self.name = name
        self.parent = parent
        self.in_ports = in_ports
        self.out_ports = out_ports
        self.cell_pos = cell_pos
        self.next_event_time = next_event_time
        self.last_event_time = last_event_time

    def initialize(self):
        return NotImplementedError()

    def int_transition(self, time):
        return NotImplementedError()

    def ext_transition(self, message):
        return NotImplementedError()

    def time_advance(self):
        return NotImplementedError()
