#!/usr/bin/env python

from setuptools import find_packages, setup

from src import openapi_parser

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
    package_data={"openapi_parser": ["py.typed"]},
    license="MIT",
    description=openapi_parser.__description__,
    keywords="swagger, python, swagger-parser, openapi3-parser, parser, openapi3, swagger-api",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
        "prance>=0.20.2",
        "openapi-spec-validator==0.6.0",
    ],
)
