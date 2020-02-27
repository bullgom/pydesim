from desim import Model, PortManager, Message, INF, NEG_INF


class Digraph(Model):

    def __init__(
            self,
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
            select=None):

        super().__init__(
            name,
            parent,
            in_ports,
            out_ports,
            cell_pos,
            next_event_time=INF,
            last_event_time=NEG_INF)

        self.children = children
        self.next_event_models = next_event_models
        self.int_couplings = int_couplings
        self.ext_output_couplings = ext_output_couplings
        self.ext_input_couplings = ext_input_couplings
        self.select = select

    def couple(self, source_port, target_port):
        coupling = None

        if source_port.model is self and target_port.model in self.children:
            coupling = self.ext_input_couplings
        elif source_port.model in self.children and target_port.model is self:
            coupling = self.ext_output_couplings
        elif source_port.model in self.children and target_port.model in self.children:
            coupling = self.int_couplings
        else:
            raise ValueError("Wrong coupling")

        if source_port in coupling:
            if target_port not in coupling[source_port]:
                coupling[source_port].append(target_port)
        else:
            coupling[source_port] = [target_port]


    def int_transition(self, time):
        result = []
        for child in self.next_event_models:
            temp = child.int_transition(time)
            if temp: result += temp

        toParent = []
        for message in result:
            for target_port in self.int_couplings[message.content.port]:
                target_port.model.ext_transition(
                    message.translate(target_port))
            for target_port in self.ext_output_couplings[message.content.port]:
                toParent.append(message.translate(target_port))

        self.time_advance()
        return toParent

    def ext_transition(self, message):
        for target_port in self.ext_input_couplings[message.content.port]:
            target_port.model.ext_transition(message.translate(target_port))
        self.time_advance()

    def time_advance(self):
        minimum = INF
        self.next_event_models.clear()
        for model in self.children:
            if model.next_event_time < minimum:
                minimum = model.next_event_time
                self.next_event_models.clear()
                self.next_event_models.append(model)
            elif model.next_event_time == minimum:
                self.next_event_models.append(model)
        self.last_event_time = self.next_event_time
        self.next_event_time = minimum

    def initialize(self):
        for child in self.children:
            child.initialize()
        self.time_advance()
