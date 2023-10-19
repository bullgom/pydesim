from pydesim import project_types as pt
from .. import port as po
from . import model as mo
import typing as ty
from . import port as pm


class Coupling(ty.DefaultDict[pm.PairedPort, list[pm.PairedPort]]):
    def __init__(self) -> None:
        super().__init__(list)

    def propagate(self, source: pm.PairedPort) -> list[pm.PairedPort]:
        """source의 값을 target에 전달한 후 반환."""
        targets = self[source]
        for target in targets:
            target.put(source.take())
        return targets


class CoupledModel(mo.Model):
    def __init__(self, in_ports: po.PortDict, out_ports: po.PortDict) -> None:
        super().__init__(in_ports, out_ports)
        self.internal_couplings: Coupling = Coupling()
        self.out_couplings: Coupling = Coupling()
        self.in_couplings: Coupling = Coupling()
        self.children: set[mo.Model] = set()

    def couple(self, source: pm.PairedPort, target: pm.PairedPort) -> None:
        """Couples two ports with direction"""
        if not (type(source) is po.Port and type(target) is po.Port):
            raise TypeError(f"You can only couple ports.")

        coupling = None

        if source.model is self and target.model in self.children:
            coupling = self.in_couplings
        elif source.model in self.children and target.model is self:
            coupling = self.out_couplings
        elif source.model in self.children and target.model in self.children:
            coupling = self.internal_couplings
        else:
            raise ValueError("Wrong coupling")

        coupling[source].append(target)

    @property
    def time_until_event(self) -> pt.VirtualTime:
        return min(self.children, key=lambda x: x.time_until_event).time_until_event
