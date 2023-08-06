from setuptools import setup, find_packages
from aicq import __version__

requirements = [
    "aiohttp",
    "pydantic"
]

setup(
    name="aicq",
    author="hdsujnb",
    version=__version__,
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.7.0'
)