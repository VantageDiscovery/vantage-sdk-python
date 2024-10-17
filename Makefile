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
	API_KEY_PART=${PYPI_API_KEY:0:10}
	@echo "Token key part: ${API_KEY_PART}"
	poetry config pypi-token.pypi "${PYPI_API_KEY}"

install: configure
	@echo "git: checking out: ${COMMIT_HASH}"
	git checkout ${COMMIT_HASH}
	@echo "Installing Python SDK dependencies"
	poetry lock --no-update
	poetry install
	@echo "Python SDK dependencies installed"

build:
	@echo "git: checking out: ${COMMIT_HASH}"
	git checkout ${COMMIT_HASH}
	@echo "Buildig Python SDK"
	poetry build

publish:
	# poetry publish -r testpypi dist/*
	@echo "Dummy publish"
