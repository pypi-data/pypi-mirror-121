from __future__ import annotations

import typing

import attr
import pyrsistent

T = typing.TypeVar("T")


@attr.dataclass(frozen=True)
class Output(typing.Generic[T]):
    path: T
    names: pyrsistent.PVector[str] = pyrsistent.pvector()


@attr.dataclass(frozen=True)
class Input(typing.Generic[T]):
    path: T

    def as_output(self, *args: str) -> Output[T]:
        return Output(self.path, pyrsistent.pvector(args))


IOType = typing.Union[Input[T], Output[T]]

IO = Input, Output


@attr.dataclass(frozen=True)
class Unwrapper(typing.Generic[T]):
    iterable: typing.Iterable[typing.Union[T, IOType[T]]]

    def inputs(self) -> typing.Iterator[T]:
        return (item.path for item in self.iterable if isinstance(item, Input))

    def outputs(
        self,
    ) -> typing.Iterator[typing.Tuple[T, typing.Sequence[str]]]:
        return (
            (item.path, item.names)
            for item in self.iterable
            if isinstance(item, Output)
        )

    def unwrapped(self) -> typing.Iterator[T]:
        return (
            item.path if isinstance(item, IO) else item
            for item in self.iterable
        )
