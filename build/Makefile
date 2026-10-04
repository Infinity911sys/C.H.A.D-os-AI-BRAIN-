.PHONY: lint test run serve site website-export website-serve

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

website-export:
	python -m chad_os.runtime.export_website

website-serve: website-export
	python -m http.server 8090 --directory website
