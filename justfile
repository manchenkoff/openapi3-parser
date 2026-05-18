#!/usr/bin/env just --justfile

set quiet

# show help
help:
    just --list

# build package
build:
    uv build

# remove temp build files
clean:
    rm -Rf dist/ .pytest_cache/ .mypy_cache/ .ruff_cache/

# upload package to test repository
publish-test:
    uv publish --index testpypi

# upload package to prod repository
publish:
    uv publish 

# install package with dependencies
sync:
    uv sync

# run unit tests
test:
    uv run pytest -qv --cov=openapi_parser --cov-report=term:skip-covered

# run package formatters
fmt:
    uv run ruff format .

# run package linters
lint:
    uv run ruff check --fix .
    uv run mypy .
    uv run ty check .
