from pathlib import Path

from setuptools import find_packages, setup

from stepizer import __version__

setup(
    name='stepizer',
    version=__version__,
    author='Mateusz Baran',
    author_email='mateusz.baran.sanok@gmail.com',
    maintainer='Mateusz Baran',
    maintainer_email='mateusz.baran.sanok@gmail.com',
    license='MIT',
    url='https://gitlab.com/mateusz.baran/stepizer',
    description='The tool for better organization of the workflow.',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.8, <4',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    extras_require={
        'dev': [
            'bump2version>=1.0.1',
            'pytest>=6.1.2',
            'pytest-cov>=2.12.1',
            'pytest-flake8>=1.0.6',
            'pytest-isort>=2.0.0',
            'pytest-mypy>=0.8.1',
            'pytest-pycodestyle>=2.2.0',
        ],
    },

)
