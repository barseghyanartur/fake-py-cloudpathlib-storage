# Update version ONLY here
VERSION := 0.1.1
SHELL := /bin/bash
UNAME_S := $(shell uname -s)
# Makefile for project
UV_RUN := uv run

.PHONY: build_docs rebuild_docs build_docs_epub build_docs_pdf serve-docs pre-commit pre-commit-install doc8 ruff ruff-fix mypy install lock lock-upgrade test test-all shell create-secrets detect-secrets clean update-version build check-build release test-release


# ----------------------------------------------------------------------------
# Documentation
# ----------------------------------------------------------------------------

# Build documentation using Sphinx and zip it
build_docs:
	$(UV_RUN) sphinx-source-tree
	$(UV_RUN) sphinx-build -n -b text docs builddocs
	$(UV_RUN) sphinx-build -n -a -b html docs builddocs
	cd builddocs && zip -r ../builddocs.zip . -x ".*" && cd ..

rebuild_docs:
	$(UV_RUN) sphinx-apidoc fakepy --implicit-namespaces --full -o docs -H 'fake-py-cloudpathlib-storage' -A 'Artur Barseghyan <artur.barseghyan@gmail.com>' -f -d 20
	cp docs/conf.py.distrib docs/conf.py
	cp docs/index.rst.distrib docs/index.rst

build_docs_epub:
	$(MAKE) -C docs/ epub SPHINXBUILD="$(UV_RUN) sphinx-build"

build_docs_pdf:
	$(MAKE) -C docs/ latexpdf SPHINXBUILD="$(UV_RUN) sphinx-build"

# Serve the built docs on port 5001
serve-docs:
	cd builddocs && $(UV_RUN) python -m http.server 5001

# ----------------------------------------------------------------------------
# Pre-commit
# ----------------------------------------------------------------------------

pre-commit:
	$(UV_RUN) pre-commit run --all-files

pre-commit-install:
	$(UV_RUN) pre-commit install

# ----------------------------------------------------------------------------
# Linting
# ----------------------------------------------------------------------------

doc8:
	$(UV_RUN) doc8

# Run ruff on the codebase
ruff:
	$(UV_RUN) ruff check .
	$(UV_RUN) ruff format --check .

ruff-fix:
	$(UV_RUN) ruff check --fix .
	$(UV_RUN) ruff format .

mypy:
	$(UV_RUN) mypy fakepy/cloudpathlib_storage/*.py

# ----------------------------------------------------------------------------
# Installation
# ----------------------------------------------------------------------------

# Install the project with all extras and dependency groups
install:
	uv sync --all-extras --all-groups

lock:
	uv lock

lock-upgrade:
	uv lock --upgrade

# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------

test: clean
	$(UV_RUN) pytest -vrx -s

test-all: test

shell:
	$(UV_RUN) ipython

# ----------------------------------------------------------------------------
# Security
# ----------------------------------------------------------------------------

create-secrets:
	$(UV_RUN) detect-secrets scan > .secrets.baseline

detect-secrets:
	$(UV_RUN) detect-secrets scan --baseline .secrets.baseline

# ----------------------------------------------------------------------------
# Development
# ----------------------------------------------------------------------------

# Clean up generated files
clean:
	find . -path ./.venv -prune -o -type f -name "*.pyc" -exec rm -f {} \;
	find . -path ./.venv -prune -o -type f -name "builddocs.zip" -exec rm -f {} \;
	find . -path ./.venv -prune -o -type f -name "*.py,cover" -exec rm -f {} \;
	find . -path ./.venv -prune -o -type f -name "*.orig" -exec rm -f {} \;
	find . -path ./.venv -prune -o -type f -name "*.db" -exec rm -f {} \;
	find . -path ./.venv -prune -o -type d -name "__pycache__" -exec rm -rf {} \; -prune
	rm -rf build/
	rm -rf dist/
	rm -rf .cache/
	rm -rf htmlcov/
	rm -rf builddocs/
	rm -rf testdocs/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf fake_py_cloudpathlib_storage.egg-info/

update-version:
	@echo "Updating version in pyproject.toml and __init__.py"
	uv version $(VERSION) --no-sync
	@if [ "$(UNAME_S)" = "Darwin" ]; then \
		gsed -i 's/__version__ = "[0-9.]\+"/__version__ = "$(VERSION)"/' fakepy/cloudpathlib_storage/__init__.py; \
	else \
		sed -i 's/__version__ = "[0-9.]\+"/__version__ = "$(VERSION)"/' fakepy/cloudpathlib_storage/__init__.py; \
	fi

# ----------------------------------------------------------------------------
# Release
# ----------------------------------------------------------------------------

build:
	uv build

check-build:
	$(UV_RUN) twine check dist/*

release:
	$(UV_RUN) twine upload dist/* --verbose

test-release:
	$(UV_RUN) twine upload --repository testpypi dist/*

%:
	@:
