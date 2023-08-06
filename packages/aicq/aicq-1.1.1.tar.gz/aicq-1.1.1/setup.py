from setuptools import setup, find_packages
from aicq import __version__

requirements = [
    "aiohttp>=3.7.4",
    "pydantic>=1.8.2"
]

setup(
    name="aicq",
    author="hdsujnb",
    version=__version__,
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.7.0'
)