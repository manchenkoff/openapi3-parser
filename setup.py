#!/usr/bin/env python

from os.path import dirname, join

from iniconfig import IniConfig
from setuptools import find_packages, setup

from src import openapi_parser

description_file = join(dirname(__file__), "readme.md")
packages = list(IniConfig("Pipfile").sections['packages'].keys())

setup(
    name=openapi_parser.__title__,
    author=openapi_parser.__author__,
    author_email=openapi_parser.__email__,
    url="https://github.com/manchenkoff/openapi3-parser",
    project_urls={
        "Source": "https://github.com/manchenkoff/openapi3-parser",
    },
    version=openapi_parser.__version__,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    license="MIT",
    description=openapi_parser.__description__,
    long_description=open(description_file).read(),
    long_description_content_type="text/markdown",
    keywords="swagger, python, version-parser, parser, version, openapi3, swagger-api",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=packages,
)
