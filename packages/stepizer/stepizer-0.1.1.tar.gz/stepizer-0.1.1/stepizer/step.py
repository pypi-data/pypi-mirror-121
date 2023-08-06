from __future__ import annotations

from functools import partial
from typing import Any, Callable, Dict, Iterable, Optional, Tuple

from stepizer.loader import Loader

ArgsType = Tuple[Any, ...]
KwargsType = Dict[str, Any]


class Step:
    def __init__(
        self,
        /,
        callable_: Callable,
        *,
        args: Optional[ArgsType] = None,
        kwargs: Optional[KwargsType] = None,
        name: Optional[str] = None,
        loader: Optional[Loader] = None,
        args_mapping: Optional[ArgsType] = None,
        kwargs_mapping: Optional[KwargsType] = None,
        is_generator: bool = False,
        cache_mode: str = 'ignore',
    ) -> None:
        self._callable = callable_

        self._args = args or tuple()
        self._kwargs = kwargs or dict()
        self._name = name or self._callable.__name__
        self._loader = loader or Loader()
        self._args_mapping = args_mapping
        self._kwargs_mapping = kwargs_mapping

        self._is_generator = is_generator
        self._cache_mode = cache_mode

        self._next_step: Optional[Step] = None

        if self._is_generator:
            self._call = self._generator
        else:
            self._call = self._function

    @property
    def callable(self) -> Callable:
        return self._callable

    @property
    def args(self) -> ArgsType:
        return self._args

    @property
    def kwargs(self) -> KwargsType:
        return self._kwargs

    @property
    def name(self) -> str:
        return self._name

    @property
    def loader(self) -> Loader:
        return self._loader

    @property
    def args_mapping(self) -> Optional[ArgsType]:
        return self._args_mapping

    @property
    def kwargs_mapping(self) -> Optional[KwargsType]:
        return self._kwargs_mapping

    @property
    def is_generator(self) -> bool:
        return self._is_generator

    @property
    def cache_mode(self) -> str:
        return self._cache_mode

    @property
    def next_step(self) -> Optional[Step]:
        return self._next_step

    def iter_steps(self) -> Iterable[Step]:
        yield self
        if self._next_step:
            yield from self._next_step.iter_steps()

    @classmethod
    def wrap(cls, callable_: Callable) -> Step:
        if isinstance(callable_, cls) and callable_._next_step is None:
            return callable_
        return cls(callable_)

    @classmethod
    def chain(cls, callable_: Callable, *callables: Callable) -> Step:
        step = cls.wrap(callable_)
        for c in callables:
            step.link(c)
        return step

    def link(self, callable_: Callable) -> Step:
        if self._next_step is None:
            self._next_step = Step.wrap(callable_)
        else:
            self._next_step.link(callable_)
        return self

    __or__ = link

    def __call__(self, *args, _cache: Optional[KwargsType] = None, **kwargs) -> Iterable[Any]:
        for outputs in self._loader(
            function=partial(self._generate_output, cache=_cache or dict()),
            outputs=self._call(*self._args, *args, **self._kwargs, **kwargs),
        ):
            yield from outputs

    def run(self, *args, **kwargs) -> Any:
        output = self(*args, **kwargs)
        if any(step._is_generator for step in self.iter_steps()):
            return list(output)
        return next(iter(output))

    def execute(self, *args, **kwargs) -> None:
        for _ in self(*args, **kwargs):
            pass

    def _map_arguments(self, output: Any, cache: KwargsType) -> Tuple[ArgsType, KwargsType]:
        if self._args_mapping is None and self._kwargs_mapping is None:
            return (output,), dict()

        args = list()
        if self._args_mapping is not None:
            for name in self._args_mapping:
                args.append(cache[name] if name else output)

        kwargs = dict()
        if self._kwargs_mapping is not None:
            for argument, name in self._kwargs_mapping.items():
                kwargs[argument] = cache[name] if name else output

        return tuple(args), kwargs

    def _update_cache(self, output: Any, cache: KwargsType) -> KwargsType:
        if self._cache_mode == 'ignore':
            return cache.copy()
        if self._cache_mode == 'add':
            return {**cache, self._name: output}
        if self._cache_mode == 'update':
            return {**cache, **output}
        raise ValueError(f"Cache mode {self._cache_mode} is not supported")

    def _generate_output(self, output: Any, cache: KwargsType) -> Iterable[Any]:
        if self._next_step is None:
            yield output
        else:
            cache = self._update_cache(output=output, cache=cache)
            args, kwargs = self._next_step._map_arguments(output=output, cache=cache)
            yield from self._next_step(*args, _cache=cache, **kwargs)

    def _function(self, *args, **kwargs) -> Iterable[Any]:
        yield self._callable(*args, **kwargs)

    def _generator(self, *args, **kwargs) -> Iterable[Any]:
        yield from self._callable(*args, **kwargs)
