# discourse-docsify

Flask extension to source data from [discourse](https://www.discourse.org/) forum posts into a [docsify](https://docsify.js.org/#/) (documentation) website.

This allows you to leverage docsify's features while still benefiting from discourse's forum nature: beautiful documentation anyone within your community may expand on and contribute to.

This project was inspired by this [canonicalwebeteam's repo](https://github.com/canonical-web-and-design/canonicalwebteam.discourse).

## Setup
Install with
```shell
pip install discourse-docsify
```

You can initialize the extension directly:
```python
from flask import Flask
from discourse_docsify import Docs

app = Flask(__name__)
# for more config options and additional parameters see below
docs = Docs(app, config={
    'DOCS_HOMEPAGE_TITLE': 'My Documentation Website',
    'DOCS_DISCOURSE_API_USERNAME': '...',
    'DOCS_DISCOURSE_API_KEY': '...',
    'DOCS_DISCOURSE_BASE_URL': '...',
    'DOCS_DISCOURSE_INDEX_TOPIC_ID': '...',
})

```

or by doing

```python
from flask import Flask
from discourse_docsify import Docs

# for more config options and additional parameters see below
docs = Docs(config={
    'DOCS_HOMEPAGE_TITLE': 'My Documentation Website',
    'DOCS_DISCOURSE_API_USERNAME': '...',
    'DOCS_DISCOURSE_API_KEY': '...',
    'DOCS_DISCOURSE_BASE_URL': '...',
    'DOCS_DISCOURSE_INDEX_TOPIC_ID': '...',
})

app = Flask(__name__)
docs.init_app(app)
```

No plugin needs to be installed on discourse, you simply need a valid API key.

### Index topic
The index topic contains the homepage content, a list of urls mappings to translate documentation paths into forum topics and the documentation sidebar.

In this topic, # headings specify the start of a section. Each of the contents described above corresponds to a specific section.
Here is the format the topic should have:
```markdown
# Homepage
Welcome to my Documentation!
        
# URLs
[details=Mapping table]
| topic | path |
| -- | -- |
| forum-url/t/general-handbook/5258 | /general-handbook |
| forum-url/t/how-to-install/5256  | /installation |
| forum-url/t/developer-api-specs/5259 | /api |
[/details]

# Navigation
[details=Navigation]
| level | path | navlink |
| -- | -- | -- |
| 1 |  | Handbooks |
| 2 | general-handbook | General Handbook |
| 1 | installation | Installation Instructions |
| 1 | api | Dev API |

[/details]
```

The names of the sections are important (`Homepage`, `URLs` and `Navigation`). 

In the URLs table, we have pairs of `topic` (forum link) and `path` (the documentation url path).

In the Navigation table, the `level` sets the indentation in the sidebar (meaning a level 2 item will be inside the level 1 item immediately above it), `path` is a path from the URLs table (or empty, if you want a linkless category) and `navlink` is the actual text in this sidebar navigation item.

## Features and Description

Discourse-Docsify will create a blueprint at the `/docs` url prefix (can be changed through the config) which will serve the files requested by docsify by fetching the forum content for the topic associated with each path.

The original topic markdown is used (and not the discourse html generated output) so you may use any docsify compatible markdown.

A caching feature is also included to speed up loading times (as querying the forum for every request can be quite slow) which may either be through a simple python dictionary or through **redis**.

Optionally, one function to be run before content is served can also be passed to the Docs object.

## The pre_content function
`Docs` accepts a third parameter: the pre_content function, a function run before each documentation request and that you may use to, for example, restrict access based on some sort of authentication:

```python
def docs_auth_validation(path):
    if 'profile' not in session:
        return redirect('/login')
    if not session['profile']['admin']:
        return abort(403, 'Only admins may view this page.')

docs = Docs(app, {...}, docs_auth_validation)
```

This function has one argument: the current request's path.

## Configuration reference

| Setting name | Default | Description | 
| --- | --- | --- | 
| DOCS_URL_PREFIX | /docs | The URL prefix for the blueprint that will be serving the docs. |
| DOCS_HOMEPAGE_TITLE | Documentation | Homepage title |
| DOCS_INDEX_PATH |  | There is a default `index.html` file with a simple docsify example, which you can replace by giving the path to your own file here. |
| DOCS_TEMPLATE_PATH |  | There is a default template to generate the documentation content (which appends edit buttons with a forum link and last updated time) but you can replace it with your own by entering its path here. |
| DOCS_HUMANIZE_LOCALE |  | [humanize](https://github.com/jmoiron/humanize) is used to generate the "last updated" strings (2 hours ago, a month ago, etc). If you want to change the language used, enter a locale name here. Example: `ru_RU` for russian. |
| DOCS_CACHE_TIMEOUT | 60 * 10 | Number of seconds for which to cache each page's content. |
| DOCS_CACHE_TYPE | memory | either `memory` (uses a simple python dictionary) or `redis` |
| DOCS_CACHE_REDIS_CONN | {} | if using redis, the redis connection arguments, [passed to the Redis constructor](https://redis-py.readthedocs.io/en/stable/#redis.Redis). |
| DOCS_CACHE_REDIS_PREFIX | discourse_docsify_docs_ | Prefix to use for redis caching |
| DOCS_DISCOURSE_API_USERNAME |  | Discourse API username. Needed to fetch forum content. |
| DOCS_DISCOURSE_API_KEY |  | Discourse API key. Needed to fetch forum content. |
| DOCS_DISCOURSE_BASE_URL |  | The discourse (forum) main url. |
| DOCS_DISCOURSE_INDEX_TOPIC_ID |  | The ID of the index topic (the number at the end of the topic url). |
