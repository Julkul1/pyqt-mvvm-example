.PHONY: start lint lint-fix format format-check test test-watch test-coverage type-check prepare release

start:
	python main.py

lint:
	flake8 app

lint-fix:
	isort app && black app

format:
	black app

format-check:
	black --check app

test:
	pytest

test-watch:
	pytest --maxfail=1 --disable-warnings --tb=short -v

test-coverage:
	pytest --cov=app

type-check:
	mypy app

prepare:
	echo "No direct husky equivalent in Python, but you can use pre-commit."

release:
	echo "Release process is project-specific." 