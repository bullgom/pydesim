import abc
import typing as ty

from . import child


class Selector(abc.ABC):
    @abc.abstractmethod
    def __call__(self, processors: ty.Sequence[child.Child]) -> child.Child:
        """Selects a single processor."""
        raise NotImplementedError


class FIFO(Selector):
    def __call__(self, processors: ty.Sequence[child.Child]) -> child.Child:
        return processors[0]
