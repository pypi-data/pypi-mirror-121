import unittest
from unittest.mock import Mock

from stepizer.loader import Loader
from stepizer.step import Step


class TestStepProperties(unittest.TestCase):
    def setUp(self) -> None:
        self.function = Mock(__name__='Mock')
        self.step = Step(self.function)

    def test_function(self) -> None:
        function = self.step.function

        self.assertIs(function, self.function)

    def test_args(self) -> None:
        args = self.step.args

        self.assertIsInstance(args, tuple)

    def test_kwargs(self) -> None:
        kwargs = self.step.kwargs

        self.assertIsInstance(kwargs, dict)

    def test_name(self) -> None:
        name = self.step.name

        self.assertIsInstance(name, str)
        self.assertEqual(self.function.__name__, name)

    def test_loader(self) -> None:
        loader = self.step.loader

        self.assertIsInstance(loader, Loader)

    def test_args_mapping(self) -> None:
        args_mapping = self.step.args_mapping

        self.assertIsInstance(args_mapping, tuple)

    def test_kwargs_mapping(self) -> None:
        kwargs_mapping = self.step.kwargs_mapping

        self.assertIsInstance(kwargs_mapping, dict)

    def test_generator(self) -> None:
        generator = self.step.generator

        self.assertIsInstance(generator, bool)
        self.assertFalse(generator)

    def test_global_output(self) -> None:
        global_output = self.step.global_output

        self.assertIsInstance(global_output, bool)
        self.assertFalse(global_output)

    def test_next_step(self) -> None:
        next_step = self.step.next_step

        self.assertIsNone(next_step)
