import abc
import typing as ty

from .. import model as mo
from .. import port as po
from . import base

CouplingMap = ty.DefaultDict[po.Port, list[tuple[base.Child, po.Port]]]


class Coordinator(base.Child[mo.CoupledModel], base.Parent):
    _owners: dict[mo.Model, base.HasModel]
    _in_map: CouplingMap
    _out_map: CouplingMap
    _internal_map: CouplingMap

    def __init__(
        self,
        model: mo.CoupledModel,
        parent: base.Parent,
        selector: base.selector.Selector = base.selector.FIFO(),
    ) -> None:
        base.Processor.__init__(self)
        base.Parent.__init__(self, selector)
        base.Child.__init__(self, model, parent)

    def star(self, current_time: float):
        imminent = self._selector(self._imminent_children)
        self._imminent_children.remove(imminent)
        imminent.star(current_time)
        self._parent.done(self, self._next_event_time)

    def x(self, t: float, port: po.Port) -> None:
        for processor, target_port in self._in_map[port]:
            target_port.put(port.consume())
            processor.x(t, target_port)
        self._parent.done(self, t)

    def y(self, t: float, ports: list[po.Port]) -> None:
        for port in ports:
            self._y(t, port)

    def _y(self, t: float, port: po.Port) -> None:
        for processor, target_port in self._internal_map[port]:
            target_port.put(port.consume())
            processor.x(t, target_port)

        to_parent: list[po.Port] = []
        for processor, target_port in self._out_map[port]:
            target_port.put(port.consume())
            to_parent.append(target_port)
        self._parent.y(t, to_parent)

    def initialize(self) -> None:
        base.Parent.initialize(self)
        base.Child.initialize(self)

        owners: dict[mo.Model, base.Child] = {
            child._model: child for child in self._children
        }

        self._in_map = self._map_couplings(self._model.in_couplings, owners)
        self._out_map = self._map_couplings(self._model.out_couplings, owners)
        self._internal_map = self._map_couplings(self._model.internal_couplings, owners)

        super().initialize()

    @staticmethod
    def _map_couplings(
        coupling: mo.coupled.Couplings, owners: dict[mo.Model, base.Child]
    ) -> CouplingMap:
        """(source port) -> (processor, target port)"""
        out = CouplingMap(list)
        for source, targets in coupling.items():
            for target_model, target_port in targets:
                processor = owners[target_model]
                out[source].append((processor, target_port))

        return out
