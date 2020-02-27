from desim import Diagraph, INF, NEG_INF, PortManager


class Simulation(Diagraph):

    def __init__(
            self,
            name,
            time_limit,
            parent=None,
            in_ports=PortManager(),
            out_ports=PortManager(),
            cell_pos=None,
            next_event_time=INF,
            last_event_time=NEG_INF,
            children=[],
            next_event_models=[],
            int_couplings={},
            ext_output_couplings={},
            ext_input_couplings={},
            select=None):

        super(Simulation, self).__init__(
            name,
            parent=None,
            in_ports=PortManager(),
            out_ports=PortManager(),
            cell_pos=None,
            next_event_time=INF,
            last_event_time=NEG_INF,
            children=[],
            next_event_models=[],
            int_couplings={},
            ext_output_couplings={},
            ext_input_couplings={},
            select=None)

        self.time_limit = time_limit

    def start_simulation(self):
        print("Initializing simulation")
        self.initialize()
        print("Starting simulation")
        while self.next_event_time <= self.time_limit and self.next_event_time != INF:
            self.int_transition(self.next_event_time)
            self.time_advance()
