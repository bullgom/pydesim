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


class port_class_iterator:
    ...


class PortClass:

    def __iter__(self) -> ty.Iterator[Port]:
        ...

    def __next__(self) -> Port:
        ...


P = ty.TypeVar("P", bound=PortClass)


def port_class(cls: type[T]) -> type[P]:
    """Make a class `port_class`."""

    for key, annotation in cls.__annotations__.items():
        origin = ty.get_origin(annotation)
        if (origin is None) or (not issubclass(origin, Port)):
            raise PortsTypeException(f"{key}: {annotation} is not a {Port.__name__}.")

    class _NewClass(cls, PortClass):
        def __init__(self: T) -> None:
            for key, annotation_type in self.__annotations__.items():
                setattr(self, key, Port())

    return _NewClass
