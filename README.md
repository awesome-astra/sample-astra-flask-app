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
