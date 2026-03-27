NAME="fly_in.py"

install:
	uv sync

run:
	uv run $(NAME)

debug:
	uv run $(NAME)

clean:
	uv cache clean
	rm -rf __pycache__ .mypy_cache .venv uv.lock

lint:
	- uv run flake8 . --exclude '.venv'
	- uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	- uv run flake8 . --exclude '.venv'
	- uv run mypy . --strict
