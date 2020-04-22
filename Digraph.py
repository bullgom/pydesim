from desim import Model, PortManager, Message, Content, INF, NEG_INF, Atomic


class Digraph(Model):

    def __init__(
            self,
            name,
            parent=None,
            cell_pos=None,
            in_ports={},
            out_ports={},
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
            last_event_time)

        self.next_event_models = []
        self.children = []
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
        
        try:
            if target_port not in coupling[source_port]:
                coupling[source_port].append(target_port)
        except KeyError:
            coupling[source_port] = [target_port]

    def int_transition(self, time):
        result = []
        for child in self.next_event_models:
            output = child.int_transition(time)
            if output: result += output
            else: break

        toParent = []
        parent_append = toParent.append
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
                    parent_append(Message(src, time, Content(target_port, value)))

        self.time_advance()
        return toParent

    def ext_transition(self, message):
        
        src = message.source
        time = message.time
        value = message.content.value
        for target_port in self.ext_input_couplings[message.content.port]:
            target_port.model.ext_transition(
                Message(src, time, Content(target_port, value)))
        self.time_advance()


    def time_advance(self):
        minimum = INF
        self.next_event_models.clear()
        append = self.next_event_models.append
        for model in self.children:
            if model.next_event_time < minimum:
                minimum = model.next_event_time
                self.next_event_models.clear()
                append(model)
            elif model.next_event_time == minimum:
                append(model)
        self.last_event_time = self.next_event_time
        self.next_event_time = minimum


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

    def find(self, name):
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

