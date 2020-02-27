from desim import Port


class PortManager(list):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __contains__(self, key):
        return any(port is key for port in self)

    def __getitem__(self, key):
        for port in self:
            if key is port.name:
                return port
        return ValueError("No such port with name: " + key)

    def __add__(self, other):
        if isinstance(other, PortManager):
            self += other.ports
        elif isinstance(other, list):
            self += other
