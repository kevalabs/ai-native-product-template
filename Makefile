PYTHON ?= python3

.PHONY: setup setup-check handoff test lint build

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

# These live checks intentionally stay separate from the offline test suite.
REPO ?= $(shell gh repo view --json nameWithOwner --jq .nameWithOwner)
BASE ?= origin/main

setup-check:
	$(PYTHON) scripts/check_github.py --repo "$(REPO)" --setup-check

handoff:
	$(PYTHON) scripts/check_github.py --repo "$(REPO)" --handoff --issue "$(ISSUE)" --base "$(BASE)"
