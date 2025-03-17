Flask-PyMongo
=============

`MongoDB <http://www.mongodb.org/>`_ is an open source database that stores
flexible JSON-like "documents," which can have any number, name, or
hierarchy of fields within, instead of rows of data as in a relational
database. Python developers can think of MongoDB as a persistent, searchable
repository of Python dictionaries (and, in fact, this is how `PyMongo
<http://api.mongodb.org/python/current/>`_ represents MongoDB documents).

Flask-PyMongo bridges Flask and PyMongo and provides some convenience
helpers.


Quickstart
----------

First, install Flask-PyMongo:

.. code-block:: bash

    $ pip install Flask-PyMongo

Next, add a :class:`~flask_pymongo.PyMongo` to your code:

.. code-block:: python

    from flask import Flask
    from flask_pymongo import PyMongo

    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
    mongo = PyMongo(app)

:class:`~flask_pymongo.PyMongo` connects to the MongoDB server running on
port 27017 on localhost, to the database named ``myDatabase``. This database
is exposed as the :attr:`~flask_pymongo.PyMongo.db` attribute.

You can use :attr:`~flask_pymongo.PyMongo.db` directly in views:

.. code-block:: python

    @app.route("/")
    def home_page():
        online_users = mongo.db.users.find({"online": True})
        return render_template("index.html", online_users=online_users)

.. note::

    Previous versions of Flask-PyMongo required that the MongoDB URI
    contained a database name; as of 2.2, this requirement is lifted. If
    there is no database name, the :attr:`~flask_pymongo.PyMongo.db`
    attribute will be ``None``.


Compatibility
-------------

Flask-PyMongo depends on recent versions of Flask and PyMongo, where "recent"
is defined to mean "was released in the last 3 years". Flask-PyMongo *may*
work with older versions, but compatibility fixes for older versions will
not be accepted, and future changes may break compatibility in older
versions.

Flask-PyMongo is tested against `supported versions
<https://www.mongodb.com/support-policy>`_ of MongoDB, and Python
and 3.9+. For the exact list of version combinations that are tested and
known to be compatible.


Helpers
-------

Flask-PyMongo provides helpers for some common tasks:

.. automethod:: flask_pymongo.wrappers.Collection.find_one_or_404

.. automethod:: flask_pymongo.PyMongo.send_file

.. automethod:: flask_pymongo.PyMongo.save_file

.. autoclass:: flask_pymongo.helpers.BSONObjectIdConverter

.. autoclass:: flask_pymongo.helpers.BSONProvider

Configuration
-------------

You can configure Flask-PyMongo either by passing a `MongoDB URI
<https://docs.mongodb.com/manual/reference/connection-string/>`_ to the
:class:`~flask_pymongo.PyMongo` constructor, or assigning it to the
``MONGO_URI`` `Flask configuration variable
<http://flask.pocoo.org/docs/1.0/config/>`_

.. note::

    Flask-PyMongo passes the connection string directly to PyMongo, so all behavior about interpretation of the connection string is determined by PyMongo itself.
    See the Connection String examples on the `PyMongo docs <https://www.mongodb.com/docs/languages/python/pymongo-driver/current/security/authentication/>`_ for more information.


The :class:`~flask_pymongo.PyMongo` instance also accepts these additional
customization options:

* ``json_options``, a :class:`~bson.json_util.JSONOptions` instance which
  controls the JSON serialization of MongoDB objects when used with
  :func:`~flask.json.jsonify`.

You may also pass additional keyword arguments to the ``PyMongo``
constructor. These are passed directly through to the underlying
:class:`~pymongo.mongo_client.MongoClient` object.

.. note::

    By default, Flask-PyMongo sets the ``connect`` keyword argument to
    ``False``, to prevent PyMongo from connecting immediately. PyMongo
    itself `is not fork-safe
    <https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/mongoclient/#forking-a-process-causes-a-deadlock>`_,
    and delaying connection until the app is actually used is necessary to
    avoid issues. If you wish to change this default behavior, pass
    ``connect=True`` as a keyword argument to ``PyMongo``.

You can create multiple ``PyMongo`` instances, to connect to multiple
databases or database servers:

.. code-block:: python

    app = Flask(__name__)

    # connect to MongoDB with the defaults
    mongo1 = PyMongo(app, uri="mongodb://localhost:27017/databaseOne")

    # connect to another MongoDB database on the same host
    mongo2 = PyMongo(app, uri="mongodb://localhost:27017/databaseTwo")

    # connect to another MongoDB server altogether
    mongo3 = PyMongo(app, uri="mongodb://another.host:27017/databaseThree")

Each instance is independent of the others and shares no state.


API
===

Classes
-------

.. autoclass:: flask_pymongo.PyMongo
   :members:

   .. attribute:: cx

      The :class:`~flask_pymongo.wrappers.MongoClient` connected to the
      MongoDB server.

   .. attribute:: db

      The :class:`~flask_pymongo.wrappers.Database` if the URI used
      named a database, and ``None`` otherwise.


Wrappers
--------

Flask-PyMongo wraps PyMongo's :class:`~pymongo.mongo_client.MongoClient`,
:class:`~pymongo.database.Database`, and
:class:`~pymongo.collection.Collection` classes, and overrides their
attribute and item accessors. Wrapping the PyMongo classes in this way lets
Flask-PyMongo add methods to ``Collection`` while allowing user code to use
MongoDB-style dotted expressions.

.. code-block:: pycon

    >>> type(mongo.cx)
    <type 'flask_pymongo.wrappers.MongoClient'>
    >>> type(mongo.db)
    <type 'flask_pymongo.wrappers.Database'>
    >>> type(mongo.db.some_collection)
    <type 'flask_pymongo.wrappers.Collection'>

.. autoclass:: flask_pymongo.wrappers.Collection(...)
   :members:



Troubleshooting
---------------

If you have problem like ``TypeError: argument must be an int, or have a fileno() method`` you should run uwsgi with the ``--wsgi-disable-file-wrapper`` flag or add the following entry in your **uwsgi.ini** file:

.. code-block:: bash

    wsgi-disable-file-wrapper = true
