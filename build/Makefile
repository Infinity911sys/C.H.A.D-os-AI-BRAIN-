.PHONY: lint test run serve

lint:
	python -m compileall chad_os tests

test:
	pytest -q

run:
	python -m chad_os.runtime.entrypoint

serve:
	python -m chad_os.runtime.entrypoint --serve
