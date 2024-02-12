.PHONY: tests

install_requirements:
	if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
	if [ -f requirements.dev.txt ]; then pip install -r requirements.dev.txt; fi

ruff:
	ruff check .

sort:
	isort --check --profile black .

tests:
	pytest .
