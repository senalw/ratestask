venv:
	python3 -m venv venv
	./venv/bin/python3 -m pip install --upgrade pip

.PHONY: setup
setup:venv
	./venv/bin/pip3 install -r requirements.txt

.PHONY: setup-style
setup-style:
	./venv/bin/pip3 install --no-cache-dir -r requirements-style.txt

.PHONY: setup-dev
setup-dev: setup setup-style setup-test

create-reports-dir:
	mkdir -p reports

.PHONY: setup-test
setup-test: setup
	./venv/bin/pip3 install -r requirements-test.txt

.PHONY: test-unit-ci
test-unit-ci: create-reports-dir
	PYTHONPATH=. \
	    ./venv/bin/pytest \
	    --cov-report xml:reports/coverage.xml \
	    --cov-report html:reports/htmlcov/ \
	    --junitxml=./reports/junit.xml \
		--cov=src \
		--full-trace \
		tests/unit/

.PHONY: check_format
check_format: #check which files will be reformatted
	./venv/bin/black --check .

.PHONY: format
format: #format files
	./venv/bin/black .

.PHONY: lint
lint:
	./venv/bin/flake8 .

.PHONY: run
run:
	PYTHONPATH=./src: ./venv/bin/python3 -m src.app

.PHONY: clean
clean:
	rm -rf venv
