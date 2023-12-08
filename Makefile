.DEFAULT_GOAL := help
.PHONY: help build test

PYPI_TOKEN := $(shell echo ${PYPI_TOKEN})
PYPI_TEST_TOKEN := $(shell echo ${PYPI_TEST_TOKEN})


build: ## Build an application
	@poetry build

configure_pypi_publishing: ## Configure publishing to PyPI
	@if [ -z "${PYPI_TOKEN}" ] ; then echo "you need to export PYPI_TOKEN before running this command" ; false ; fi
	@if [ -z "${PYPI_TOKEN}" ] ; then echo "you need to export PYPI_TEST_TOKEN before running this command" ; false ; fi
	@poetry config repositories.test-pypi https://test.pypi.org/legacy/
	@poetry config pypi-token.test-pypi $(PYPI_TEST_TOKEN)
	@poetry config pypi-token.pypi $(PYPI_TOKEN)

publish-test: ## Upload package to test PyPI
	@poetry publish -r test-pypi

publish: build ## Upload package to PyPI
	@poetry publish
	@make clean

install: build ## Install application to Poetry environment
	@poetry install

clean: ## Remove build files
	@rm -Rf build/ dist/ *.egg-info .pytest_cache/ .mypy_cache/ .pytype/ .eggs/ src/*.egg-info
	@echo "Temporary files were clear"

test: ## Run code tests
	@poetry run pytest

lint: ## Run code linters
	@echo "Run code linters..."
	@poetry run mypy ./src

help: ## Show this message
	@echo "Application management"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
