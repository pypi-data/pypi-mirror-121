from functools import partial
from multiprocessing import Pool
from typing import Any, Callable, Iterable, List, Optional


class Loader:
    def __call__(self, function: Callable, outputs: Iterable[Any]) -> Iterable[Any]:
        yield from map(function, outputs)


class BatchLoader(Loader):
    def __init__(self, batch_size: int, collate: Optional[Callable] = None) -> None:
        self._batch_size = batch_size
        self._collate = collate

    def collate(self, outputs: List[Any]) -> Any:
        if self._collate is None:
            return outputs
        return self._collate(outputs)

    def __call__(self, function: Callable, outputs: Iterable[Any]) -> Iterable[Any]:
        batch = []
        for raw_output in outputs:
            batch.append(raw_output)
            if len(batch) == self._batch_size:
                outputs = self.collate(batch)
                yield function(outputs)
                batch = []

        if batch:
            outputs = self.collate(batch)
            yield function(outputs)


class MultiprocessingLoader(Loader):
    @staticmethod
    def function(function: Callable, output: Any) -> List[Any]:
        return list(function(output))

    def __call__(self, function: Callable, outputs: Iterable[Any]) -> Iterable[Any]:
        with Pool() as pool:
            yield from pool.imap(partial(self.function, function), outputs)
