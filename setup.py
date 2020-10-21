from os.path import dirname, join

from setuptools import find_packages, setup

from src import swagger_parser

description_file = join(dirname(__file__), "readme.md")

setup(
    name=swagger_parser.__title__,
    author=swagger_parser.__author__,
    author_email=swagger_parser.__email__,
    url="https://github.com/manchenkoff/swagger-parser",
    project_urls={
        "Source": "https://github.com/manchenkoff/swagger-parser",
    },
    version=swagger_parser.__version__,
    packages=find_packages(where="src/swagger_parser"),
    license="MIT",
    description=swagger_parser.__description__,
    long_description=open(description_file).read(),
    long_description_content_type="text/markdown",
    keywords="swagger, python, swagger-parser, parser, openapi, swagger-api",
    install_requires=[
        "prance",
        "openapi-spec-validator",
    ],
)
