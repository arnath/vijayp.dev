# vijayp.dev

This is the repo for my personal website, [vijayp.dev](https://www.vijayp.dev). It's written using
plain HTML and CSS (there's actually no Javascript at all), along with a single Python build script
that converts my blog posts from Markdown to HTML and creates the blog index page.

## Usage

This repo uses make and [uv](https://docs.astral.sh/uv/) as build tools. Any other tools (including
Python) will be automatically fetched by the commands below. Once you have those, there are only two
commands:

- `make build` - Builds the site and outputs it into the `dist/` folder.
- `make serve` - Uses Python's `http.server` to serve the website at `http://localhost:8080`.
