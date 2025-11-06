PYTHON ?= python3
PKG_DIR := .

.PHONY: test dev-install reinstall build fmt lint bump-patch bump-minor bump-major clean clean-pyc

## Run the test suite
test:
	$(PYTHON) -m pytest -q

## Editable install (recommended while developing)
dev-install:
	$(PYTHON) -m pip install -e . --no-build-isolation

## Reinstall editable (force refresh)
reinstall:
	-$(PYTHON) -m pip uninstall -y name-format
	$(MAKE) dev-install

## Build sdist/wheel
build:
	$(PYTHON) -m build

## Format with Black
fmt:
	$(PYTHON) -m black name_format tests

## Lint with Ruff
lint:
	$(PYTHON) -m ruff check name_format tests

## Clean Python junk
clean-pyc:
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
	find . -name "*.pyc" -delete -o -name "*.pyo" -delete

## Clean build + test artifacts
clean: clean-pyc
	rm -rf .pytest_cache *.egg-info build dist
