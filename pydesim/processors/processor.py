import abc

import pydantic as da
import typing_extensions as te

from .. import constants as const
from .. import port as po


class Processor(abc.ABC):
    def __init__(self, in_ports: po.PortDict, out_ports: po.PortDict) -> None:
        self.next_event_time: da.NonNegativeFloat = const.INF
        self.last_event_time: da.NonNegativeFloat = const.INF
        self.in_ports: po.PortDict = in_ports
        self.out_ports: po.PortDict = out_ports
