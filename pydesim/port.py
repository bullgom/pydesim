import itertools
import typing as ty

T = ty.TypeVar("T")


class Port(ty.Generic[T]):
    _id: int
    _name: str
    _value: T | None

    __id_gen: ty.ClassVar[itertools.count] = itertools.count()

    def __init__(self, name: str):
        self._name: str = name
        self._id = next(self.__id_gen)
        self._value = None

    def put(self, value: T) -> None:
        self._value = value

    def consume(self) -> T:
        self._value, out = None, self._value
        if not out:
            raise ValueError(f"Tried to consume an empty port {self}.")
        return out

    def __eq__(self, other) -> bool:
        if isinstance(other, Port):
            return self._id == other._id
        else:
            raise NotImplementedError()

    def __hash__(self) -> int:
        return self._id

    @property
    def has_value(self) -> bool:
        return bool(self._value)
