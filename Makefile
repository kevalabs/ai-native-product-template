PYTHON ?= python3

.PHONY: setup test lint build

setup:
	git config core.hooksPath .githooks

# Extend these targets with the product's tests, lint, and build at bootstrap.
test: lint build
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

lint:
	git diff --check
	git diff --cached --check
	sh -n .githooks/pre-commit

build:
	$(PYTHON) scripts/verify_template.py
