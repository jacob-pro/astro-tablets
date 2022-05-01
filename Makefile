.PHONY: clean
clean:
	rm -rf ./venv

venv:
	python -m venv ./venv
	pip install -r requirements.txt
	pip install -r test_requirements.txt

.PHONY: test
test: venv
	flake8 src/
	mypy src/
	pytest src/ -v
	python src/cli.py --help

.PHONY: format
format:
	black src/
	isort src/
