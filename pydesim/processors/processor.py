import abc

import pydantic as da
import typing_extensions as te

from .. import constants as const
from .. import port as po
from ..models import base_model as mo


class Processor(abc.ABC):
    def __init__(self, model: mo.Model) -> None:
        self.next_event_time: da.NonNegativeFloat = const.INF
        self.last_event_time: da.NonNegativeFloat = const.INF
        self.__model = model
