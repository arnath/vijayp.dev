import os
import shutil
from pathlib import Path

import pandoc
from frontmatter import Frontmatter

OUTPUT_DIRECTORY = os.getenv("BUILD_DIR", "dist/")
POST_SNIPPET = """
<div class="post">
    <a href="/blog/{slug}/"><h3>{title}</h3></a>
    <div class="subtext">{date}</div>
</div>
"""
JOB_SNIPPET = """
<a href="{link}" target="_blank">
    <div class="job-card">
        <p><b>{title}</b></p>
        <p class="subtext">{team}</p>
        <p class="subtext">{location}</p>
        <p class="subtext">{postDate}</p>
    </div>
</a>
"""


def build_apple_job_search():
    shutil.copyfile(
        "src/lib/better-apple-job-search/jobs.json",
        os.path.join(OUTPUT_DIRECTORY, "projects/better-apple-job-search/jobs.json"),
    )


def build_blog():
    # Load post template.
    with open("src/lib/blog/post-template.html", "r") as file:
        post_template = file.read()

    posts_directory = Path("src/lib/blog/posts")
    post_dates = []
    post_html_snippets = []
    for file in posts_directory.glob("*.md"):
        slug = Path(file).stem

        # Read the frontmatter to get the title, date, and publish status.
        post = Frontmatter.read_file(file)
        title = post["attributes"]["title"]
        date = post["attributes"]["date"].strftime("%B %-d, %Y")

        # Convert the doc to HTML with Pandoc.
        doc = pandoc.read(file=file, format="markdown+yaml_metadata_block")
        meta = doc[0]
        print(meta)
        formatted_content = pandoc.write(doc, format="html+yaml_metadata_block")
        post_html = post_template.format(
            title=title,
            date=date,
            content=formatted_content,
        )

        # If the post isn't published, skip it.
        if not post["attributes"]["published"]:
            continue

        # Generate the HTML snippet for this post's link on the blog index.
        post_html_snippets.append(
            POST_SNIPPET.format(slug=slug, title=title, date=date)
        )
        post_dates.append(post["attributes"]["date"])

        # Write the formatted post to the output directory.
        post_path = os.path.join(OUTPUT_DIRECTORY, "blog", slug)
        os.makedirs(post_path, exist_ok=True)
        with open(os.path.join(post_path, "index.html"), "w") as file:
            file.write(post_html)

    # Sort the post snippets by descending date.
    sorted_pairs = sorted(zip(post_dates, post_html_snippets), reverse=True)
    sorted_snippets = [pair[1] for pair in sorted_pairs]

    # Write the blog index HTML.
    with open("src/lib/blog/index-template.html", "r") as file:
        index_template = file.read()
    index_html = index_template.format(posts=str.join("\n", sorted_snippets))
    with open(os.path.join(OUTPUT_DIRECTORY, "blog", "index.html"), "w") as file:
        file.write(index_html)


def build():
    # This script writes output to the dist/ directory. If the directory exists,
    # delete it.
    if os.path.exists(OUTPUT_DIRECTORY):
        shutil.rmtree(OUTPUT_DIRECTORY)

    # Copy src/static to dist/.
    shutil.copytree("src/static/", OUTPUT_DIRECTORY)

    build_blog()
    build_apple_job_search()


if __name__ == "__main__":
    build()
