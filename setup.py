from os.path import dirname, join

import swagger_parser
from setuptools import find_packages, setup

description_file = join(dirname(__file__), 'readme.txt')

setup(
    name="swagger_parser",
    author="Artyom Manchenkov",
    author_email="artyom@manchenkoff.me",
    url="https://github.com/manchenkoff/swagger-parser",
    version=swagger_parser.__version__,
    packages=find_packages(),
    license="MIT",
    long_description=open(description_file).read()
)
