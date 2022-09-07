# Sample Astra DB Flask app

This minimal API illustrates a good pattern to integrate Astra DB
as the backing storage for your Flask applications.

You can run it yourself by following the instructions given below
or just use it as a reference when writing your own API.

### Setup

First make sure you have an [Astra DB instance](https://awesome-astra.github.io/docs/pages/astra/create-instance/)
up and running.
Have the ["Token"](https://awesome-astra.github.io/docs/pages/astra/create-token/)
and the ["secure connect bundle"](https://awesome-astra.github.io/docs/pages/astra/download-scb/) zipfile
ready
(see the links for more details).

Make the secrets and the connection details available by copying
the `.env.sample` file to a new `.env` and customizing it. This
will be picked up by the API on startup (no need to `source` the
file thanks to the `python-dotenv` utility).

Next you need some Python dependencies. Preferrably in a virtual environment,
run the following:

```
pip install -r requirements.txt
```

> Please stick to Python version 3.7 or higher.

Your Astra DB instance is brand new: in order to create the
table needed by the API and populate it with a few sample rows,
you can simply launch the provided initialization script once:
```
python storage/db_initialize.py
```

> This step, which will also serve as test of the connection to Astra DB,
> has the sole purpose of making this demo application self-contained:
> in a production setup, you'll probably want to
> handle schema changes in a more controlled way.


### Run and test the API

You're ready to go: start the API with

```
flask --app api run --reload
```

and, in a separate console, you can test the endpoints with the following
`curl` commands:


```
curl -s \
  localhost:5000/animal/Vanessa/atalanta \
  -H 'Content-Type: application/json' \
  | jq

curl -s \
  localhost:5000/animal/Vanessa \
  -H 'Content-Type: application/json' \
  | jq

curl -s -X POST \
  localhost:5000/animal \
  -d '{"genus":"Philaeus", "species":"chrysops", "image_url":"https://imgur.com/F66x0Pt", "size_cm":0.12, "sightings":2, "taxonomy": ["Arthropoda","Arachnida","Aranea","Salticidae"]}' \
  -H 'Content-Type: application/json' \
  | jq

curl -s \
  localhost:5000/plant/Plantago \
  -H 'Content-Type: application/json' \
  | jq
# by trying with `curl -i -s ...` and no jq piping one can
# see that this has "Transfer-Encoding: chunked".
```

### Remarks

The database session is handled as a process-wide singleton
using a global cache, as per best practices with the Cassandra driver.

Likewise, to optimize performance, a global cache of prepared statement
is used throughout the API
(more precisely, there is one such cache per each Flask worker process).

On the Flask side, the code here takes advantage of Flask's application-context
[`g` object](https://flask.palletsprojects.com/en/2.2.x/api/#flask.g)
and the [`before_request` hook](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.before_request) to make sure each request will find a reference
to the (one and only) database session, ready for use as `g.session`.
_(Alternatively, for example only when few endpoints need the database,
one could simply have a `session = get_session()` in the endpoint function's
code and call it a day.)_

This API uses Pydantic for validation and handling of request/response
data types. However, this requires some manual plumbing, as can be seen in the
code:

- to validate/cast the POST request payload, a `animal = Animal(**request.get_json())` is wrapped in a try/except construct, in order to return a meaningful error (from Pydantic) and a status 422 ("unprocessable entity") if anything is off. **Note**: `request` is a Flask abstraction;
- when returning responses, one must explicitly `jsonify` not directly the Pydantic object, rather its `.dict()` representation. So, for example, `return jsonify(animal.dict())`. **Note**: `jsonify` is a Flask primitive, whole `.dict()` is a built-in method for Pydantic models.

In case your response is very long, the API endpoint function may want to
return a `Chunked` response and construct it piece-by-piece as it fetches data
from the database. More precisely, the Cassandra driver will handle DB-side
pagination transparently and simply present the stream of results as an iterator;
the API code, on the response-side, will stream the response piecewise using
Flask's [streaming responses](https://flask.palletsprojects.com/en/2.2.x/patterns/streaming/).
This amounts to returning a `(generator, headers)` pair in the endpoint, and
taking care of manually constructing, piecewise, a syntactically correct
JSON on top of the stream of results that keep pouring in from the driver.
