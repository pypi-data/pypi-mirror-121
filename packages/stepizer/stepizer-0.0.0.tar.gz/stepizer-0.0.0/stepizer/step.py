from __future__ import annotations

from functools import partial
from typing import Any, Callable, Iterable, Optional, Tuple

from stepizer.loader import Loader


class Step:
    def __init__(
        self,
        function: Callable,
        *,
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
        name: Optional[str] = None,
        loader: Optional[Loader] = None,
        args_mapping: Optional[tuple] = None,
        kwargs_mapping: Optional[dict] = None,
        generator: bool = False,
        global_output: bool = False,
    ) -> None:
        self._function = function

        self._name = name or function.__name__
        self._loader = loader or Loader()
        self._args = args or tuple()
        self._kwargs = kwargs or dict()
        self._args_mapping = args_mapping or tuple()
        self._kwargs_mapping = kwargs_mapping or dict()

        self._generator = generator
        self._global_output = global_output

        self._next_step: Optional[Step] = None

    @property
    def function(self) -> Callable:
        return self._function

    @property
    def args(self) -> tuple:
        return self._args

    @property
    def kwargs(self) -> dict:
        return self._kwargs

    @property
    def name(self) -> str:
        return self._name

    @property
    def loader(self) -> Loader:
        return self._loader

    @property
    def args_mapping(self) -> tuple:
        return self._args_mapping

    @property
    def kwargs_mapping(self) -> dict:
        return self._kwargs_mapping

    @property
    def generator(self) -> bool:
        return self._generator

    @property
    def global_output(self) -> bool:
        return self._global_output

    @property
    def next_step(self) -> Optional[Step]:
        return self._next_step

    def append(self, function: Callable) -> Step:
        step = function if isinstance(function, Step) else Step(function)

        if step._next_step:
            raise ValueError(f"Step {step._name} cannot have successor")

        if step._name == self._name:
            raise ValueError(f"Step name {step._name} is duplicated")

        if self._next_step is None:
            self._next_step = step
        else:
            self._next_step.append(step)

        return self

    __or__ = append

    def _map_arguments(self, output: Any, global_outputs: dict) -> Tuple[tuple, dict]:
        args = list()
        kwargs = dict()

        if self._args_mapping or self._kwargs_mapping:
            for step_name in self._args_mapping:
                args.append(global_outputs[step_name] if step_name else output)

            for arg_name, step_name in self._kwargs_mapping.items():
                kwargs[arg_name] = global_outputs[step_name] if step_name else output
        else:
            args.append(output)

        return tuple(args), kwargs

    def _update_global_outputs(self, output: Any, global_outputs: dict) -> dict:
        global_outputs = global_outputs.copy()
        if self._global_output:
            global_outputs[self._name] = output
        return global_outputs

    def _generate_outputs_from_function(self, *args, **kwargs) -> Iterable[Any]:
        output = self._function(*self._args, *args, *self._kwargs, **kwargs)
        if self._generator:
            yield from output
        else:
            yield output

    def _generate_outputs_from_next_step(self, output: Any, global_outputs: dict) -> Iterable[Any]:
        if self._next_step is None:
            yield output
        else:
            args, kwargs = self._next_step._map_arguments(output, global_outputs)
            global_outputs = self._update_global_outputs(output, global_outputs)
            yield from self._next_step(*args, _global_outputs=global_outputs, **kwargs)

    def __call__(self, *args, _global_outputs: Optional[dict] = None, **kwargs) -> Iterable[Any]:
        global_outputs = _global_outputs or dict()
        for outputs in self._loader(
            function=partial(self._generate_outputs_from_next_step, global_outputs=global_outputs),
            outputs=self._generate_outputs_from_function(*args, **kwargs),
        ):
            yield from outputs

    def iter_steps(self) -> Iterable[Step]:
        yield self
        if self._next_step:
            yield from self._next_step.iter_steps()

    def run(self, *args, **kwargs) -> Any:
        output = self(*args, **kwargs)
        if any(step._generator for step in self.iter_steps()):
            return list(output)
        return next(iter(output))

    def execute(self, *args, **kwargs) -> None:
        for _ in self(*args, **kwargs):
            pass
