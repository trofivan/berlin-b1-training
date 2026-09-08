.PHONY: setup build preview

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

build:
	.venv/bin/python scripts/build_site.py

preview: build
	.venv/bin/python -m http.server 8000 --directory dist
