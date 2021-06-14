
---


---

Goat is a **Python fast, scalable, light-weight synchronous web framework** that makes building performant and highly concurrent web APIs fun and accessible to everyone.

## Requirements

Python 3.6+

## Installation

```bash
pip install goat
```

## Example

```python
from api import API

app = API()

@app.route("/")
def index(req, res):
    res.json = {"hello": "world"}
```

Save this as `app.py`, then start a [gunicorn](https://gunicorn.org/) server (hot reload enabled!):

```bash
gunicorn app:app --reload
```

Say hello!

```bash
$ curl http://localhost:8000
{"hello": "world"}
```



