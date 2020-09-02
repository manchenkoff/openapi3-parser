from os.path import dirname, join

from setuptools import find_packages, setup

import swagger_parser

description_file = join(dirname(__file__), "readme.md")

setup(
    name="swagger_parser",
    author="Artyom Manchenkov",
    author_email="artyom@manchenkoff.me",
    url="https://github.com/manchenkoff/swagger-parser",
    project_urls={
        "Source": "https://github.com/manchenkoff/swagger-parser",
    },
    version=swagger_parser.__version__,
    packages=find_packages(where="swagger_parser"),
    license="MIT",
    description="Swagger API v3 parser",
    long_description=open(description_file).read(),
    long_description_content_type="text/markdown",
    keywords="swagger, python, swagger-parser, parser, openapi, swagger-api",
    install_requires=[
        "prance",
        "openapi-spec-validator",
    ],
)
