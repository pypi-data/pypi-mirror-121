import unittest
from unittest.mock import Mock

from stepizer.loader import Loader
from stepizer.step import Step


class TestStepProperties(unittest.TestCase):
    def setUp(self) -> None:
        self.callable = Mock(__name__='Mock')
        self.step = Step(self.callable)

    def test_callable(self) -> None:
        function = self.step.callable

        self.assertIs(function, self.callable)

    def test_args(self) -> None:
        args = self.step.args

        self.assertIsInstance(args, tuple)

    def test_kwargs(self) -> None:
        kwargs = self.step.kwargs

        self.assertIsInstance(kwargs, dict)

    def test_name(self) -> None:
        name = self.step.name

        self.assertIsInstance(name, str)
        self.assertEqual(self.callable.__name__, name)

    def test_loader(self) -> None:
        loader = self.step.loader

        self.assertIsInstance(loader, Loader)

    def test_args_mapping(self) -> None:
        args_mapping = self.step.args_mapping

        self.assertIsNone(args_mapping)

    def test_kwargs_mapping(self) -> None:
        kwargs_mapping = self.step.kwargs_mapping

        self.assertIsNone(kwargs_mapping)

    def test_is_generator(self) -> None:
        generator = self.step.is_generator

        self.assertIsInstance(generator, bool)
        self.assertFalse(generator)

    def test_cache_mode(self) -> None:
        cache_mode = self.step.cache_mode

        self.assertIsInstance(cache_mode, str)
        self.assertEqual('ignore', cache_mode)

    def test_next_step(self) -> None:
        next_step = self.step.next_step

        self.assertIsNone(next_step)
