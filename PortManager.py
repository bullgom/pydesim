from pydesim import Port


class PortManager(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __contains__(self, key):
        return any(port is key for port in self)

    def __add__(self, other):
        if isinstance(other, PortManager):
            for key, value in other.items():
                self[key] = value
        elif isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
