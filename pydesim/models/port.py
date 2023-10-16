import dataclasses as dc
from .. import port as po
from . import base_model as bm
import typing_extensions as te

class PairedPort(po.Port):
    
    def __init__(self, model: bm.BaseModel) -> None:
        super().__init__()
        self.model : bm.BaseModel = model
