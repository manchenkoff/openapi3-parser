.DEFAULT_GOAL := help
.PHONY: help build test

build: ## Build an application
	@pipenv run python setup.py sdist
	@pipenv run python setup.py bdist_wheel

publish-test: ## Upload package to test PyPI
	@pipenv run twine upload --repository testpypi dist/*

publish: build ## Upload package to PyPI
	@pipenv run twine upload dist/*
	@make clean

install: build ## Install application to Pip environment
	@pipenv run python setup.py install

install-dev: ## Install application to Pip development environment
	@pipenv run python setup.py develop
	@make clean

run: ## Run application entrypoint
	@pipenv run python src/

clean: ## Remove build files
	@rm -Rf build/ dist/ *.egg-info .pytest_cache/ .eggs/ src/*.egg-info

test: ## Run code tests
	@pipenv run python -m pytest -q

sync: ## Sync with Pipfile packages list
	@pipenv sync

help: ## Show this message
	@echo "Application management"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'