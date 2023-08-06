from typing import Generic, Optional

from pyffect._types import T


class Option(Generic[T]):

    def __init__(self, value: T, *, _force: bool = False) -> None:
        if not _force:
            raise TypeError(
                'Cannot directly initialize, '
                'please either Some or NONE'
            )
        self._value = value
        self._type = type(self)

    @property
    def isEmpty(self) -> bool:
        return self._value is None

    @property
    def isDefined(self) -> bool:
        return self._value is not None

    @property
    def value(self) -> T:
        if self._value is None:
            raise ValueError('Value is NONE.')
        else:
            return self._value

    def getOrElse(self, value: Optional[T]) -> T:
        if self._value is not None:
            return self._value
        else:
            return value

    @classmethod
    def fromValue(cls, val: Optional[T]) -> 'Option[T]':
        return NONE() if val is None else Some(val)

    def __eq__(self, other: T):  # type: ignore
        return isinstance(other, self._type) and self._value == other._value


class NONE(Option):  # type: ignore

    def __init__(self) -> None:
        super().__init__(None, _force=True)


class Some(Option[T]):
    def __init__(self, value: T) -> None:
        super().__init__(value, _force=True)
