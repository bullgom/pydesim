import dataclasses as dc
import typing as ty
import typing_extensions as te

VirtualTime = float

T = ty.TypeVar("T")


class State(ty.Generic[T]):
    __value: T

    def __init__(self, value: T) -> None:
        super().__init__()
        self.__value = value

    @classmethod
    def initialize(cls, initial_value: T) -> te.Self:
        return cls(initial_value)

    def set(self, value: T) -> None:
        self.__value = value

    def get(self) -> T:
        return self.__value
