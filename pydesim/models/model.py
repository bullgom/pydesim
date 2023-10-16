from .. import port as po
from . import base_model as bm
from . import port as mp

PairedPortDict = dict[str, mp.PairedPort]


class Model(bm.BaseModel):
    def __init__(self, in_ports: po.PortDict, out_ports: po.PortDict) -> None:
        super().__init__()
        self.in_ports: PairedPortDict = {k: mp.PairedPort(self) for k in in_ports}
        self.out_ports: PairedPortDict = {k: mp.PairedPort(self) for k in out_ports}
