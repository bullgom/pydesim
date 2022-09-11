from . import Digraph, INF, NEG_INF, PortManager
import time

class Simulation(Digraph):

    def __init__(
            self,
            name,
            time_limit=INF,
            parent=None,
            in_ports=[],
            out_ports=[],
            cell_pos=None,
            next_event_time=INF,
            last_event_time=NEG_INF,
            int_couplings={},
            ext_output_couplings={},
            ext_input_couplings={},
            select=None):

        super().__init__(
            name,
            parent,
            cell_pos,
            in_ports,
            out_ports,
            next_event_time,
            last_event_time,
            int_couplings,
            ext_output_couplings,
            ext_input_couplings,
            select)

        self.time_limit = time_limit

    def start_simulation(self):
        print("Initializing simulation")
        self.initialize()
        print("Starting simulation")
        start_time = time.time()
        while self.next_event_time <= self.time_limit and self.next_event_time != INF:
            self.int_transition(self.next_event_time)
            self.time_advance()
        print("Simulation finished\nRunning Time: "+str( time.time()-start_time))
