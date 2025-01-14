---
title: Rewriting my website in plain HTML and CSS
date: 2025-01-15
published: true
---

This week, I decided to rewrite my website using plain HTML and CSS. When I [originally made
it][agio], I used SvelteKit for simplicity. It was a more interesting project than I was expecting
when I started working so I wanted to share my thoughts on the experience.

### Why?

There are a number of reasons I decided to do the rewrite. One is that I'm currently unemployed so I
have a lot of free time for side projects. Another is that, as you can see, this website is pretty
simple so I wasn't gaining a lot from using SvelteKit. I also wanted to move the site over to
Cloudflare Pages so this was an opportune time to make some changes.

However, the primary reason I decided to make some changes is that I find the Javascript bundler and
building ecosystem _incredibly_ aggravating to use. For example, one of the things I set up my old
website to do was build the blog section from the set of Markdown posts. I assumed this would be
easy to do. SvelteKit and Vite allow you to prerender your website and I had a set of files at build
time - I just needed to add some logic to transform them. Instead, it was infuriatingly difficult to
figure out a way to just get a handle to a set of files in my tree at build time (let me caveat that
I'm not a frontend dev and maybe I missed something obvious). It took me hours of Googling and
trying out different options to come up with this awful piece of code that worked to load the
contents of a file and give them to my page:

```
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params }) => {
  const file = await import(
    `../../../../lib/assets/posts/${params.slug}.md`
  );

  return { content: file.default, ...file.metadata };
};
```

I was tired of dealing with things like this for the tiny amount I was gaining from using SvelteKit.
And so, I finally decided it was time for a rewrite.

### How?

I think spending too much time on Hacker News gave me the misconception that writing a website using
plain HTML and CSS would be a relatively well-paved path in 2025. I spent some time looking around
for guides or a "canonical" way of doing this and found that there isn't really one. Because of
that, I decided to just start from scratch with an empty directory and go from there. My website is
small enough that I was able to remake a lot of the pages as static HTML.

However, I prefer writing blog posts in Markdown. It's easier to write than HTML, I can pull posts
out of my existing Obsidian vault, and I just find it more convenient. Therefore, I needed some kind
of script to turn my Markdown blog posts into HTML content. I investigated some options for this and
found [Pandoc][pandoc]. Pandoc is a universal document converter for converting markup formats. It
provides a library and a CLI for converting documents from Markdown to HTML (along with many other
formats).

To write the script, I wanted something as lightweight as possible but easier to use than a Bash
script. This led me to Python and [uv][uv]. I've found that uv basically abstracts away the Python
environment in a way that's really convenient for a tiny project like this. Using Python also gave
me a free way to serve my website using the `http.server` module. Finally, I wrote a tiny Makefile
so I wouldn't have to remember the serve command.

### Results

The [outcome][repo] was not the _most_ revolutionary because my website was really simple in the
first place. But the size of my "compiled" website asset went from ~356kb to ~88kb. My project tree
got a lot simpler and the only Javascript on the site now is to highlight code. I'm also just
happier about the state of things. I feel like I understand how and why my site works (where before
I understood parts but not the whole mystery).

<table>
  <thead style="vertical-align: bottom; text-align: center;">
    <tr>
      <td><i class="subtext" style="font-size: 14px;">Before, with SvelteKit</i></td>
      <td><i class="subtext" style="font-size: 14px;">After, with plain HTML</i></td>
    </tr>
  </thead>
  <tbody style="vertical-align: top; text-align: center;">
    <tr>
      <td><img src="./before.png" /></td>
      <td><img src="./after.png" /></td>
  </tbody>
</table>

### Next Steps

There are two downsides that I've found so far. I'd like to investigate ways to fix or improve
these.

- More code duplication. SvelteKit has a component system so I could make my navigation bar as a
  component and reuse it. When I removed it, I had to duplicate that code in a few places. Luckily
  the cost was pretty minor because I only really have four HTML pages. I'm aware that there's some
  way to do this using web components. It's something I intend to look into as one of my next side
  projects.
- No live reloading. I have to kill the website to rebuild it now. I'm sure there's a tool I can
  find to fix this, or maybe just use something like FastAPI that has automatic reload. But until I
  do something about it, there's a minor added cost every time I make a change.

Also, I think this repository is now a reasonably good template for someone who wants to make a
simple website with some Markdown blog posts without using a generator. I was surprised when I
started this project how difficult it was to find a guide about how to write your site without a
framework. Hopefully this can help some other people.

[agio]: https://github.com/arnath/arnath.github.io
[pandoc]: https://pandoc.org/
[uv]: https://docs.astral.sh/uv/
[repo]: https://github.com/arnath/vijayp.dev
