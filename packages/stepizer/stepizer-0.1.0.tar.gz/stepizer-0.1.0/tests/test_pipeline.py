import unittest
from typing import Iterable

from stepizer.step import Step


def read_paths(directory: str) -> Iterable[str]:
    for i in range(len(directory)):
        yield f'{directory}/image_{i}.jpg'


def read_image(path: str) -> list:
    return [ord(char) for char in path]


def detect_faces(image: list) -> Iterable[list]:
    for i in range(0, len(image), 7):
        yield image[i:i + 7]


def save(face: list, path: str = 'None') -> str:
    return path + f'.{sum(face)}.save'


class TestPipeline(unittest.TestCase):
    def setUp(self) -> None:
        self.pipeline = (
            Step(read_paths, is_generator=True, cache_mode='add')
            | read_image
            | Step(detect_faces, is_generator=True)
            | Step(save, args_mapping=('', 'read_paths'))
        )

    def test_pipeline(self) -> None:
        expected = [
            'dir/image_0.jpg.677.save',
            'dir/image_0.jpg.611.save',
            'dir/image_0.jpg.103.save',
            'dir/image_1.jpg.677.save',
            'dir/image_1.jpg.612.save',
            'dir/image_1.jpg.103.save',
            'dir/image_2.jpg.677.save',
            'dir/image_2.jpg.613.save',
            'dir/image_2.jpg.103.save',
        ]

        actual = self.pipeline.run('dir')

        self.assertListEqual(expected, actual)
