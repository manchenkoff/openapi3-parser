#!/usr/bin/env python

from os.path import dirname, join

from setuptools import find_packages, setup

from src import openapi_parser

description_file = join(dirname(__file__), "readme.md")

setup(
    name=openapi_parser.__title__,
    author=openapi_parser.__author__,
    author_email=openapi_parser.__email__,
    url="https://github.com/manchenkoff/openapi-parser",
    project_urls={
        "Source": "https://github.com/manchenkoff/openapi-parser",
    },
    version=openapi_parser.__version__,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    license="MIT",
    description=openapi_parser.__description__,
    long_description=open(description_file).read(),
    long_description_content_type="text/markdown",
    keywords="swagger, python, openapi-parser, parser, openapi, openapi3, swagger-api",
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
        "prance",
        "openapi-spec-validator",
    ],
)
