.PHONY: lint test run

lint:
	python -m compileall -q chad_os tests

test:
	python -m pytest -q

run:
	python -m chad_os.runtime.entrypoint
