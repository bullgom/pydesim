import abc
from .. import project_types as pt
from .. import port as po

"""
A basic `model` contains following information:
- The set of input ports through which external events are received
- The set of output ports through which external events are sent
- The set of state variables and parameters (where `sigma` is a common variable used to denote the
  time until next event.)
- The time advance function which controls the timing of internal transitions. When the `sigma` 
  variable is present, this function just returns the value of `sigma`.
- 
"""


class Model(abc.ABC):
    _in_ports: po.PortClass
    _out_ports: po.PortClass
    _sigma: pt.VirtualTime  # time until next event

    def time_advance(self) -> pt.VirtualTime:
        return self._sigma

    @abc.abstractmethod
    def internal_transition(self, state: pt.State, current: pt.VirtualTime) -> pt.State:
        pass

    @property
    def in_ports(self) -> po.PortClass:
        return self._in_ports

    @property
    def out_ports(self) -> po.PortClass:
        return self._out_ports
