
class Port:
    def __init__(self, model, name):
        self.model = model
        self.name = name

    def __eq__(self, other):
        if isinstance(other, Port):  return (self.name == other.name and self.model is other.model)
        else: return NotImplemented

    def __hash__(self):
        return hash((self.model, self.name))
