import typing as ty
import dataclasses as dc


class PortException(Exception):
    """Exceptions related to ports."""


class NoValueException(PortException):
    def __init__(self, details: str = "") -> None:
        super().__init__(f"Tried to take value from port when it was empty!\n{details}")


class PortsTypeException(PortException):
    def __init__(self, details: str = "") -> None:
        super().__init__(
            f"Only `Port`s are allowed as attribute of a `port_class`.\n{details}"
        )


PortName: ty.TypeAlias = str

T = ty.TypeVar("T")


class Port(ty.Generic[T]):
    def __init__(self) -> None:
        super().__init__()
        self.__value: T | None = None

    def put(self, value: T) -> None:
        self.__value = value

    def take(self) -> T:
        if self.__value is None:
            raise NoValueException()
        output = self.__value
        self.__value = None
        return output


class PortDict(dict[str, Port]):
    pass
