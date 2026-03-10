lint:
	uv run ruff check

lintfix: format
	uv run ruff check --fix

format:
	uv run ruff format
