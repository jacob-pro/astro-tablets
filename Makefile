.PHONY: clean
clean:
	rm -rf ./venv

venv:
	python -m venv ./venv
	pip install -r requirements.txt
	pip install -r test_requirements.txt

.PHONY: test
test: venv
	mypy src/
	pytest src/ -v

