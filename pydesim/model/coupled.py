import typing as ty

from pydesim import port as po

from .. import port as po
from . import model as mo


class Couplings(ty.DefaultDict[po.Port, list[tuple[mo.Model, po.Port]]]):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(list, *args, **kwargs)


class CoupledModel(mo.Model):
    _children: list[mo.Model]
    in_couplings: Couplings
    out_couplings: Couplings
    internal_couplings: Couplings

    def __init__(self, name: str):
        super().__init__(name)
        self._children = []
        self.in_couplings = Couplings()
        self.out_couplings = Couplings()
        self.internal_couplings = Couplings()

    def add_child(self, child: mo.Model) -> None:
        self._children.append(child)

    def add_children(self, *children: mo.Model) -> None:
        self._children += children

    def external(self, elapsed_time: float, port: po.Port) -> None:
        ...

    def internal(self, current_time: float):
        ...

    def initialize(self) -> float:
        times = [child._remaining_time for child in self._children]
        self.hold_for(min(times))
        return self._remaining_time

    def output(self) -> list[po.Port]:
        ...
