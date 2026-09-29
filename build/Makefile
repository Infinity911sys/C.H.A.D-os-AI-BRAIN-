.PHONY: lint test run serve site

lint:
	python -m compileall chad_os tests

test:
	pytest -q

run:
	python -m chad_os.runtime.entrypoint

serve:
	python -m chad_os.runtime.entrypoint --serve

site:
	python -m chad_os.runtime.entrypoint --serve
