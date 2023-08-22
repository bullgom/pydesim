import typing as ty

from .. import port as po
from . import model as mo


class Couplings(ty.DefaultDict[po.Port, list[tuple[mo.Model, po.Port]]]):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(list, *args, **kwargs)


class CoupledModel(mo.Model):
    _children: list[mo.Model]
    _in_couplings: Couplings
    _out_couplings: Couplings
    _internal_couplings: Couplings
