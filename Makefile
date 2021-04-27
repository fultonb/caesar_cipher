.PHONY: test

pdf:
	asciidoctor-pdf README.adoc

test:
	pytest -xv test.py

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache
