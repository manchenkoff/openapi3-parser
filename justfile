#!/usr/bin/env just --justfile

set quiet := true

# show help
help:
    just --list

# build package
build:
    uv build

# remove temp build files
clean:
    rm -Rf dist/ .pytest_cache/ .mypy_cache/

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
    uv run pytest -qv

# run package linters
lint:
    uv run mypy ./src 
