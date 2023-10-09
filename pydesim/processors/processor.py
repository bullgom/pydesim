import abc

import pydantic as da
import typing_extensions as te

from .. import constants as const
from ..content import Content
from .. import models as mo


class Processor(abc.ABC):
    def __init__(self, model: mo.Model) -> None:
        self.next_event_time: da.NonNegativeFloat = const.INF
        self.last_event_time: da.NonNegativeFloat = const.INF
        self.model: mo.Model = model
