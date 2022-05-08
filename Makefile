.PHONY: clean
clean:
	rm -rf ./venv

venv:
	python -m venv ./venv
	pip install -r requirements.txt
	pip install -r test_requirements.txt

.PHONY: check
check: venv
	mypy src/
	flake8 src/

.PHONY: test
test: venv check
	pytest src/ -v

.PHONY: format
format: venv
	black src/
	isort src/
