import abc
from .. import project_types as pt
from .. import port as po

"""
A basic `model` contains following information:
- The set of input ports through which external events are received
"""

class Model(abc.ABC):
    _input_ports: set[po.Port]
    
    @abc.abstractmethod
    def internal_transition(self, state: pt.State, current: pt.VirtualTime) -> pt.State:
        pass
    
    @abc.abstractmethod
    def external_transition(self, state: pt.State, elapsed: pt.VirtualTime, )