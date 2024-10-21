sources = vantage_sdk
COMMIT_HASH=$(GIT_HASH)

.PHONY: test format lint unittest coverage pre-commit clean
test: format lint unittest

format:
	isort $(sources) tests
	black $(sources) tests

lint:
	flake8 $(sources) tests
	mypy $(sources) tests

unittest:
	pytest

coverage:
	pytest --cov=$(sources) --cov-branch --cov-report=term-missing tests

pre-commit:
	pre-commit run --all-files

clean:
	rm -rf .mypy_cache .pytest_cache
	rm -rf *.egg-info
	rm -rf .tox dist site
	rm -rf coverage.xml .coverage

configure:
	poetry config pypi-token.pypi "${PYPI_API_KEY}"

install:
	@echo "Installing Python SDK dependencies"
	poetry lock --no-update
	poetry install
	@echo "Python SDK dependencies installed"

build:
	@echo "Buildig Python SDK"
	poetry build

publish:
	poetry publish
