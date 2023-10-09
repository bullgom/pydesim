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
    in_ports: po.PortDict
    out_ports: po.PortDict
    _sigma: pt.VirtualTime  # time until next event

    def time_advance(self) -> pt.VirtualTime:
        return self._sigma

    @abc.abstractmethod
    def internal_transition(self, state: pt.State, current: pt.VirtualTime) -> pt.State:
        pass

    @abc.abstractmethod
    def external_transition(
        self, state: pt.State, elapsed: pt.VirtualTime, input: po.Port
    ) -> pt.State:
        pass
