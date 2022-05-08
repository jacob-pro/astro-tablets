ifeq ($(OS),Windows_NT)
	VENV_BIN = venv/Scripts
else
	VENV_BIN = venv/bin
endif

.PHONY: clean
clean:
	rm -rf ./venv

venv:
	python -m venv ./venv

# A file used to track when the requirements were last installed
venv/requirements: requirements.txt test_requirements.txt venv
	${VENV_BIN}/pip install -r requirements.txt
	${VENV_BIN}/pip install -r test_requirements.txt
	touch venv/requirements

.PHONY: check
check: venv/requirements
	${VENV_BIN}/mypy src/
	${VENV_BIN}/flake8 src/

.PHONY: test
test: venv/requirements check
	${VENV_BIN}/pytest src/ -v

.PHONY: format
format: venv/requirements
	${VENV_BIN}/black src/
	${VENV_BIN}/isort src/
