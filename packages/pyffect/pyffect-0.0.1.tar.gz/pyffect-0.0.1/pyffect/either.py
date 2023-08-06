from __future__ import annotations

from typing import Generic, Union, Optional

from pyffect._types import E
from pyffect.option import T, NONE, Some, Option


class Either(Generic[T, E]):

    def __init__(self, left: Optional[T], right: Optional[E], *, _force: bool = False) -> None:
        if not _force:
            raise TypeError(
                'Cannot directly initialize, '
                'please use Left or Right.'
            )
        if left is None and right is None:
            raise ValueError('both cannot be none')

        if left is not None and right is not None:
            raise ValueError('both cannot be not none')

        self._left = left
        self._right = right
        self._type = type(self)

    @property
    def isLeft(self) -> bool:
        return self._left is not None

    @property
    def isRight(self) -> bool:
        return self._right is not None

    @property
    def leftValue(self) -> T:
        if self.isRight:
            raise ValueError('this is not Left')
        assert self._left is not None
        return self._left

    @property
    def rightValue(self) -> E:
        if self.isLeft:
            raise ValueError('this is not Right')
        assert self._right is not None
        return self._right

    @property
    def toOption(self) -> Option[E]:
        if self.isRight:
            assert self._right is not None
            return Some(self._right)
        else:
            return NONE()

    def __eq__(self, other: Union[Left, Right]):  # type: ignore
        return isinstance(other, self._type) and (self._left == other._left and self._right == other._right)


class Left(Either[E, T]):
    def __init__(self, value: E) -> None:
        assert value is not None
        super().__init__(right=None, left=value, _force=True)


class Right(Either[E, T]):
    def __init__(self, value: T) -> None:
        assert value is not None
        super().__init__(right=value, left=None, _force=True)
