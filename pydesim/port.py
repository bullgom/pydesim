import typing as ty
import dataclasses as dc


class PortException(Exception):
    """Exceptions related to ports."""


class NoValueTakeException(PortException):
    def __init__(self, details: str = "") -> None:
        super().__init__(f"Tried to take value from port when it was empty!\n{details}")


class NonPortTypeInAttributeException(PortException):
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
            raise NoValueTakeException()
        output = self.__value
        self.__value = None
        return output


def port_class(cls: type[T]):
    """
    Make a class `port_class`.
    A 
    """
    for key, annotation_type in cls.__annotations__.items():
        if isinstance(annotation_type, Port):
            raise NonPortTypeInAttributeException(
                f"{key}:{annotation_type} is not a `Port`."
            )
            
    def __init__(self: T, *args, **kwargs) -> None:
        for key, annotation_type in cls.__annotations__.items():
            setattr(self, key, Port())

    cls.__init__ = __init__ #

    return cls