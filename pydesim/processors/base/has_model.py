import typing as ty

from ... import model as mo

_M = ty.TypeVar("_M", bound=mo.Model)


class HasModel(ty.Generic[_M]):
    _model: _M

    def __init__(self, model: _M) -> None:
        super().__init__()
        self._model = model

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._model.__repr__()})"
