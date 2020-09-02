.DEFAULT_GOAL := help
.PHONY: help build

build: ## Build an application
	@pipenv run python setup.py sdist
	@pipenv run python setup.py bdist_wheel

publish-test: ## Upload package to test PyPI
	@pipenv run twine upload --repository testpypi dist/*

publish: ## Upload package to PyPI
	@pipenv run twine upload dist/*

install: ## Install application to Pip environment
	@pipenv run python setup.py install

clean: ## Remove build files
	@rm -Rf build/ dist/ *.egg-info

test: ## Run code tests
	@pipenv run pytest -q

sync: ## Sync with Pipfile packages list
	@pipenv sync

help: ## Show this message
	@echo "Application management"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'