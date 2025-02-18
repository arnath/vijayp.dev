---
title: I downloaded Apple's jobs data because I hate their search UI
date: 2025-02-04
published: true
---

_TL;DR: I downloaded the data from Apple's careers site because their search UI infuriates me. The
raw data is available here: [`jobs.json`](./jobs.json). The data was last updated 2025-02-018._

As I mentioned in [my last blog post](../rewrite-plain-html/), I'm currently unemployed and spending
a lot of time job searching. I would obviously love to apply to some roles at Apple but I find their
careers website infuriating to use.

### Issues with the website

To set the stage, Apple's Careers site is [here.][apple] There's two main things that bother me
personally. <br /><br />

![Location is required](./location-required.png)

For one, there's no way to search across all locations. This likely doesn't affect most people but
I'm currently in a unique life situation where I'm looking for jobs in multiple countries. This also
makes it difficult to tell what locations Apple has jobs in unless you go elsewhere and look up the
possible options. Note that it _does_ have a country filter, which is why I say this probably
affects me more than most people.<br /><br />

![Engineers could fall under a lot of these](./teams.png)

The other thing that drives me crazy is that there's no way to get it to show me jobs of a certain
category, like "software engineering". I can filter by team, except as shown above engineers could
fall under a bunch of different categories here. Or I can add keyword filters, but this requires me
to try a bunch of searches to catch all the different ways job titles can be written. Apple uses a
_lot_ of these, including Software Engineer, SWE, AI/ML Engineer, Hardware Engineer, Network
Engineer, etc. I'm not saying these are all jobs I'm looking at personally - just all jobs that
someone might come to this website and have an expectation of seeing.

### Getting the data

As usual in situations like this, I started with the browser developer tools. I thought that the
location limitation was imposed by the UI but unfortunately it turns out that this is a requirement
of the underlying API. The search calls out to this API:

```bash
POST https://jobs.apple.com/api/role/search

{
    "query": The query string,
    "locale": Locale (I used en-us everywhere),
    "filters": {
        "postingpostLocation": [List of location IDs (see below)]
    },
    "page": Page number, starting at 1
}
```

For United States (the default location for me), the location ID value is `postLocation-USA`, so
it's not something obvious like the international country code. This meant that I needed to get the
location IDs for locations I cared about. When you type in the Location box on their search page, it
performs find-as-you-type lookups. These call out to this API:

```bash
GET https://jobs.apple.com/api/v1/refData/postlocation?input={query}
```

Unfortunately, this API returns an array of results, sometimes even if you type in a full location
name. As such, I had to do some manual work to collate the locations. The "Work at Apple" page has a
list of locations on it so I fed them into this API, grabbed the results, and manually cleaned it
up. I eventually had the realization that if you query for a country, it will give you _all_ the
results for that country without querying for individual cities. This let me whittle the list down
to what's in [`locations.json`](./locations.json).<br /><br />

![Apple's location list](./locations.png)

After that, it was pretty quick work to actually call the API and get the data. The logic to do this
lives in the [`get_apple_jobs.py`](https://github.com/arnath/vijayp.dev/blob/main/get_apple_jobs.py)
script if you want to play with it.

### Trying to and eventually giving up on doing something with the data

The jobs data I downloaded is in [`jobs.json`](./jobs.json). When I originally started playing with
this, I wanted to put together a simple web app that surfaced the data. I went through a bunch of
iteration on it (you can see some of it in the commit history of [this PR][pr]). However, the core
feature was basically searching the jobs data and it turns out that doing that naively (case
insensitive string contains) on 4000 jobs while you type is too much for your browser to handle
without causing performance issues.

While I could have solved this by implementing something more complicated than just searching on
some in-memory JSON, nothing I came up with really seemed worth the amount of effort it would take.
This is especially true because I'm not a frontend dev and I'd have to learn at least part of this
as I do it.

As such, I decided to just publish the data and let you do what you want with it. It's JSON so it's
really easy to, for example, load it into the Python interpreter to run a small query:

```python
import json

with open("jobs.json", "r") as file:
    jobs = json.loads(file.read())
    europe_jobs = [
        j for j in jobs if j["locations"][0]["countryName"] in [
            "Ireland",
            "Spain",
            "Germany",
            "United Kingdom",
            "Denmark",
            "Ireland",
            "Czechia",
            "Sweden",
            "Switzerland",
            "France"
        ]
    ]
```

I actually ran this because it was useful to me personally so I saved the output. That data is in
[`jobs-europe.json`](./jobs-europe.json). Hopefully this is helpful to someone. Happy job hunting!

[apple]: https://jobs.apple.com/en-us
[pr]: https://github.com/arnath/vijayp.dev/pull/2
