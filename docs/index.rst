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
        return render_template("index.html",
            online_users=online_users)

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
and 3.8+. For the exact list of version combinations that are tested and
known to be compatible, see the `envlist` in `tox.ini
<https://github.com/dcrosta/flask-pymongo/blob/master/tox.ini>`_.


Helpers
-------

Flask-PyMongo provides helpers for some common tasks:

.. automethod:: flask_pymongo.wrappers.Collection.find_one_or_404

.. automethod:: flask_pymongo.PyMongo.send_file

.. automethod:: flask_pymongo.PyMongo.save_file

.. autoclass:: flask_pymongo.helpers.BSONObjectIdConverter

.. autoclass:: flask_pymongo.helpers.JSONEncoder

Configuration
-------------

You can configure Flask-PyMongo either by passing a `MongoDB URI
<https://docs.mongodb.com/manual/reference/connection-string/>`_ to the
:class:`~flask_pymongo.PyMongo` constructor, or assigning it to the
``MONGO_URI`` `Flask configuration variable
<http://flask.pocoo.org/docs/1.0/config/>`_

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
    <http://api.mongodb.com/python/current/faq.html#is-pymongo-fork-safe>`_,
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

.. code-block:: python

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


History and Contributors
------------------------

Changes:

- 2.4.0: Unreleased

  - `#125 <https://github.com/dcrosta/flask-pymongo/pull/125>`_ Drop
    MongoDB 3.2 support.
  - `#130 <https://github.com/dcrosta/flask-pymongo/pull/130>`_ Fix
    quickstart example in README (Emmanuel Arias).
  - `#62 <https://github.com/dcrosta/flask-pymongo/issues/62>`_ Add
    support for :func:`~flask.json.jsonify()`.
  - `#131 <https://github.com/dcrosta/flask-pymongo/pulls/131>`_ Drop
    support for Flask 0.11 and Python 3.4; Add support for MongoDB 4.2,
    PyMongo 3.9, and Flask 1.1.

- 2.3.0: April 24, 2019

  - Update version compatibility matrix in tests, drop official support for
    PyMongo less than 3.3.x.

- 2.2.0: November 1, 2018

  - `#117 <https://github.com/dcrosta/flask-pymongo/pull/117>`_ Allow URIs
    without database name.

- 2.1.0: August 6, 2018

  - `#114 <https://github.com/dcrosta/flask-pymongo/pull/114>`_ Accept
    keyword arguments to :meth:`~flask_pymongo.PyMongo.save_file` (Andrew C.
    Hawkins).

- 2.0.1: July 17, 2018

  - `#113 <https://github.com/dcrosta/flask-pymongo/pull/113>`_ Make the
    ``app`` argument to ``PyMongo`` optional (yarobob).

- 2.0.0: July 2, 2018

  **This release is not compatible with Flask-PyMongo 0.5.x or any earlier
  version.** You can see an explanation of the reasoning and changes in
  `issue #110 <https://github.com/dcrosta/flask-pymongo/issues/110>`_.

  - Only support configuration via URI.
  - Don't connect to MongoDB by default.
  - Clarify version support of Python, Flask, PyMongo, and MongoDB.
  - Readability improvement to ``README.md`` (MinJae Kwon).

- 0.5.2: May 19, 2018

  - `#102 <https://github.com/dcrosta/flask-pymongo/pull/102>`_ Return 404,
    not 400, when given an invalid input to `BSONObjectIdConverter` (Abraham
    Toriz Cruz).

- 0.5.1: May 24, 2017

  - `#93 <https://github.com/dcrosta/flask-pymongo/pull/93>`_ Supply a
    default ``MONGO_AUTH_MECHANISM`` (Mark Unsworth).

- 0.5.0: May 21, 2017

    **This will be the last 0.x series release.** The next non-bugfix
    release will be Flask-PyMongo 2.0, which will introduce backwards
    breaking changes, and will be the foundation for improvements and
    changes going forward. Flask-PyMongo 2.0 will no longer support Python
    2.6, but will support Python 2.7 and Python 3.3+.

  - `#44 <https://github.com/dcrosta/flask-pymongo/issues/44>`_, `#51
    <https://github.com/dcrosta/flask-pymongo/pull/51>`_ Redirect ``/``
    to ``/HomePage`` in the wiki example (David Awad)
  - `#76 <https://github.com/dcrosta/flask-pymongo/pull/76>`_ Build on more
    modern Python versions (Robson Roberto Souza Peixoto)
  - `#79 <https://github.com/dcrosta/flask-pymongo/pull/79>`_, `#84
    <https://github.com/dcrosta/flask-pymongo/issues/84>`_, `#85
    <https://github.com/dcrosta/flask-pymongo/pull/85>`_ Don't use
    ``flask.ext`` import paths any more (ratson, juliascript)
  - `#40 <https://github.com/dcrosta/flask-pymongo/issues/40>`_, `#83
    <https://github.com/dcrosta/flask-pymongo/pull/83>`_, `#86
    <https://github.com/dcrosta/flask-pymongo/pull/86>`_ Fix options parsing
    from ``MONGO_URI`` (jobou)
  - `#72 <https://github.com/dcrosta/flask-pymongo/issues/72>`_, `#80
    <https://github.com/dcrosta/flask-pymongo/pull/80>`_ Support
    ``MONGO_SERVER_SELECTION_TIMEOUT_MS`` (Henrik Blidh)
  - `#34 <https://github.com/dcrosta/flask-pymongo/issues/34>`_, `#64
    <https://github.com/dcrosta/flask-pymongo/pull/64>`_, `#88
    <https://github.com/dcrosta/flask-pymongo/pull/88>`_ Support
    from ``MONGO_AUTH_SOURCE`` and ``MONGO_AUTH_MECHANISM`` (Craig Davis)
  - `#74 <https://github.com/dcrosta/flask-pymongo/issues/74>`_, `#77
    <https://github.com/dcrosta/flask-pymongo/issues/77>`_, `#78
    <https://github.com/dcrosta/flask-pymongo/pull/78>`_ Fixed ``maxPoolSize``
    in PyMongo 3.0+ (Henrik Blidh)
  - `#82 <https://github.com/dcrosta/flask-pymongo/issues/82>`_ Fix "another
    user is already authenticated" error message.
  - `#54 <https://github.com/dcrosta/flask-pymongo/issues/54>`_ Authenticate
    against "admin" database if no ``MONGO_DBNAME`` is provided.

- 0.4.1: January 25, 2016

  - Add the connect keyword:
    `#67 <https://github.com/dcrosta/flask-pymongo/pull/67>`_.

- 0.4.0: October 19, 2015

  - Flask-Pymongo is now compatible with pymongo 3.0+:
    `#63 <https://github.com/dcrosta/flask-pymongo/pull/63>`_.

- 0.3.1: April 9, 2015

  - Flask-PyMongo is now tested against Python 2.6, 2.7, 3.3, and 3.4.
  - Flask-PyMongo installation now no longer depends on `nose
    <https://pypi.python.org/pypi/nose/>`_.
  - `#58 <https://github.com/dcrosta/flask-pymongo/pull/58>`_ Update
    requirements for PyMongo 3.x (Emmanuel Valette).
  - `#43 <https://github.com/dcrosta/flask-pymongo/pull/43>`_ Ensure error
    is raised when URI database name is parsed as 'None' (Ben Jeffrey).
  - `#50 <https://github.com/dcrosta/flask-pymongo/pull/50>`_ Fix a bug in
    read preference handling (Kevin Funk).
  - `#46 <https://github.com/dcrosta/flask-pymongo/issues/46>`_ Cannot use
    multiple replicaset instances which run on different ports (Mark
    Unsworth).
  - `#30 <https://github.com/dcrosta/flask-pymongo/issues/30>`_
    ConfiguationError with MONGO_READ_PREFERENCE (Mark Unsworth).

- 0.3.0: July 4, 2013

  - This is a minor version bump which introduces backwards breaking
    changes! Please read these change notes carefully.
  - Removed read preference constants from Flask-PyMongo; to set a
    read preference, use the string name or import constants directly
    from :class:`pymongo.read_preferences.ReadPreference`.
  - `#22 (partial) <https://github.com/dcrosta/flask-pymongo/pull/22>`_
    Add support for ``MONGO_SOCKET_TIMEOUT_MS`` and
    ``MONGO_CONNECT_TIMEOUT_MS`` options (ultrabug).
  - `#27 (partial) <https://github.com/dcrosta/flask-pymongo/pull/27>`_
    Make Flask-PyMongo compatible with Python 3 (Vizzy).

- 0.2.1: December 22, 2012

  - `#19 <https://github.com/dcrosta/flask-pymongo/pull/19>`_ Added
    ``MONGO_DOCUMENT_CLASS`` config option (jeverling).

- 0.2.0: December 15, 2012

  - This is a minor version bump which may introduce backwards breaking
    changes! Please read these change notes carefully.
  - `#17 <https://github.com/dcrosta/flask-pymongo/pull/17>`_ Now using
    PyMongo 2.4's ``MongoClient`` and ``MongoReplicaSetClient`` objects
    instead of ``Connection`` and ``ReplicaSetConnection`` classes
    (tang0th).
  - `#17 <https://github.com/dcrosta/flask-pymongo/pull/17>`_ Now requiring
    at least PyMongo version 2.4 (tang0th).
  - `#17 <https://github.com/dcrosta/flask-pymongo/pull/17>`_ The wrapper
    class ``flask_pymongo.wrappers.Connection`` is renamed to
    ``flask_pymongo.wrappers.MongoClient`` (tang0th).
  - `#17 <https://github.com/dcrosta/flask-pymongo/pull/17>`_ The wrapper
    class ``flask_pymongo.wrappers.ReplicaSetConnection`` is renamed to
    ``flask_pymongo.wrappers.MongoReplicaSetClient`` (tang0th).
  - `#18 <https://github.com/dcrosta/flask-pymongo/issues/18>`_
    ``MONGO_AUTO_START_REQUEST`` now defaults to ``False`` when
    connecting using a URI.

- 0.1.4: December 15, 2012

  - `#15 <https://github.com/dcrosta/flask-pymongo/pull/15>`_ Added support
    for ``MONGO_MAX_POOL_SIZE`` (Fabrice Aneche)

- 0.1.3: September 22, 2012

  - Added support for configuration from MongoDB URI.

- 0.1.2: June 18, 2012

  - Updated wiki example application
  - `#14 <https://github.com/dcrosta/flask-pymongo/issues/14>`_ Added
    examples and docs to PyPI package.

- 0.1.1: May 26, 2012

  - Added support for PyMongo 2.2's "auto start request" feature, by way
    of the ``MONGO_AUTO_START_REQUEST`` configuration flag.
  - `#13 <https://github.com/dcrosta/flask-pymongo/pull/13>`_ Added
    BSONObjectIdConverter (Christoph Herr)
  - `#12 <https://github.com/dcrosta/flask-pymongo/pull/12>`_ Corrected
    documentation typo (Thor Adam)

- 0.1: December 21, 2011

  - Initial Release


Contributors:

- `jeverling <https://github.com/jeverling>`_
- `tang0th <https://github.com/tang0th>`_
- `Fabrice Aneche <https://github.com/akhenakh>`_
- `Thor Adam <https://github.com/thoradam>`_
- `Christoph Herr <https://github.com/jarus>`_
- `Mark Unsworth <https://github.com/markunsworth>`_
- `Kevin Funk <https://github.com/k-funk>`_
- `Ben Jeffrey <https://github.com/jeffbr13>`_
- `Emmanuel Valette <https://github.com/karec>`_
- `David Awad <https://github.com/DavidAwad>`_
- `Robson Roberto Souza Peixoto <https://github.com/robsonpeixoto>`_
- `juliascript <https://github.com/juliascript>`_
- `Henrik Blidh <https://github.com/hbldh>`_
- `jobou <https://github.com/jbouzekri>`_
- `Craig Davis <https://github.com/blade2005>`_
- `ratson <https://github.com/ratson>`_
- `Abraham Toriz Cruz <https://github.com/categulario>`_
- `MinJae Kwon <https://github.com/mingrammer>`_
- `yarobob <https://github.com/yarobob>`_
- `Andrew C. Hawkins <https://github.com/achawkins>`_
