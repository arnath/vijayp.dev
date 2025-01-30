.PHONY: build serve get-apple-jobs

build:
	uv run build.py

serve:
	uv run python -m http.server 8080 --directory dist

get-apple-jobs:
	uv run get_apple_jobs.py
