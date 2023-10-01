import pydantic as dan

VirtualTime = dan.NonNegativeFloat

@dan.dataclasses.dataclass
class State:
    pass