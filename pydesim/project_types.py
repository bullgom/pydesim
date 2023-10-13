import dataclasses as dc
import typing as ty
import typing_extensions as te

VirtualTime = float

T = ty.TypeVar("T")

@dc.dataclass
class State:
    """Model should have a subclass of State as a attribute."""
    time_until_event: VirtualTime