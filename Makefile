.PHONY: tests

install_requirements:
	pip3 install -r requirements.txt

ruff:
	ruff check .

tests:
	pytest .