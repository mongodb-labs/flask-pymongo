# Changelog

## 3.1.0: Unreleased

- TDB

## 3.0.1 Jan 29, 2025

- Fix inclusion of `_version.py` file.

## 3.0.0: Jan 29, 2025

- Support Flask 3.0+ and PyMongo 4.0+.
- Support Python 3.9-3.13.
- Support MongoDB 4.4+.
- Add support for `~flask.json.jsonify()`.

## 2.3.0: April 24, 2019

- Update version compatibility matrix in tests, drop official support
  for PyMongo less than 3.3.x.

## 2.2.0: November 1, 2018

- [#117](https://github.com/dcrosta/flask-pymongo/pull/117) Allow
  URIs without database name.

## 2.1.0: August 6, 2018

- [#114](https://github.com/dcrosta/flask-pymongo/pull/114) Accept
  keyword arguments to `~flask_pymongo.PyMongo.save_file` (Andrew C.
  Hawkins).

## 2.0.1: July 17, 2018

- [#113](https://github.com/dcrosta/flask-pymongo/pull/113) Make the
  `app` argument to `PyMongo` optional (yarobob).

## 2.0.0: July 2, 2018

**This release is not compatible with Flask-PyMongo 0.5.x or any
earlier version.** You can see an explanation of the reasoning and
changes in [issue
#110](https://github.com/dcrosta/flask-pymongo/issues/110).

- Only support configuration via URI.
- Don't connect to MongoDB by default.
- Clarify version support of Python, Flask, PyMongo, and MongoDB.
- Readability improvement to `README.md` (MinJae Kwon).

## 0.5.2: May 19, 2018

- [#102](https://github.com/dcrosta/flask-pymongo/pull/102) Return
  404, not 400, when given an invalid input to
  <span class="title-ref">BSONObjectIdConverter</span> (Abraham Toriz
  Cruz).

## 0.5.1: May 24, 2017

- [#93](https://github.com/dcrosta/flask-pymongo/pull/93) Supply a
  default `MONGO_AUTH_MECHANISM` (Mark Unsworth).

## 0.5.0: May 21, 2017

> **This will be the last 0.x series release.** The next non-bugfix
> release will be Flask-PyMongo 2.0, which will introduce backwards
> breaking changes, and will be the foundation for improvements and
> changes going forward. Flask-PyMongo 2.0 will no longer support
> Python 2.6, but will support Python 2.7 and Python 3.3+.

- [#44](https://github.com/dcrosta/flask-pymongo/issues/44),
  [#51](https://github.com/dcrosta/flask-pymongo/pull/51) Redirect
  `/` to `/HomePage` in the wiki example (David Awad)
- [#76](https://github.com/dcrosta/flask-pymongo/pull/76) Build on
  more modern Python versions (Robson Roberto Souza Peixoto)
- [#79](https://github.com/dcrosta/flask-pymongo/pull/79),
  [#84](https://github.com/dcrosta/flask-pymongo/issues/84),
  [#85](https://github.com/dcrosta/flask-pymongo/pull/85) Don't use
  `flask.ext` import paths any more (ratson, juliascript)
- [#40](https://github.com/dcrosta/flask-pymongo/issues/40),
  [#83](https://github.com/dcrosta/flask-pymongo/pull/83),
  [#86](https://github.com/dcrosta/flask-pymongo/pull/86) Fix options
  parsing from `MONGO_URI` (jobou)
- [#72](https://github.com/dcrosta/flask-pymongo/issues/72),
  [#80](https://github.com/dcrosta/flask-pymongo/pull/80) Support
  `MONGO_SERVER_SELECTION_TIMEOUT_MS` (Henrik Blidh)
- [#34](https://github.com/dcrosta/flask-pymongo/issues/34),
  [#64](https://github.com/dcrosta/flask-pymongo/pull/64),
  [#88](https://github.com/dcrosta/flask-pymongo/pull/88) Support
  from `MONGO_AUTH_SOURCE` and `MONGO_AUTH_MECHANISM` (Craig Davis)
- [#74](https://github.com/dcrosta/flask-pymongo/issues/74),
  [#77](https://github.com/dcrosta/flask-pymongo/issues/77),
  [#78](https://github.com/dcrosta/flask-pymongo/pull/78) Fixed
  `maxPoolSize` in PyMongo 3.0+ (Henrik Blidh)
- [#82](https://github.com/dcrosta/flask-pymongo/issues/82) Fix
  "another user is already authenticated" error message.
- [#54](https://github.com/dcrosta/flask-pymongo/issues/54)
  Authenticate against "admin" database if no `MONGO_DBNAME` is
  provided.

## 0.4.1: January 25, 2016

- Add the connect keyword:
  [#67](https://github.com/dcrosta/flask-pymongo/pull/67).

## 0.4.0: October 19, 2015

- Flask-Pymongo is now compatible with pymongo 3.0+:
  [#63](https://github.com/dcrosta/flask-pymongo/pull/63).

## 0.3.1: April 9, 2015

- Flask-PyMongo is now tested against Python 2.6, 2.7, 3.3, and 3.4.
- Flask-PyMongo installation now no longer depends on
  [nose](https://pypi.python.org/pypi/nose/).
- [#58](https://github.com/dcrosta/flask-pymongo/pull/58) Update
  requirements for PyMongo 3.x (Emmanuel Valette).
- [#43](https://github.com/dcrosta/flask-pymongo/pull/43) Ensure
  error is raised when URI database name is parsed as 'None' (Ben
  Jeffrey).
- [#50](https://github.com/dcrosta/flask-pymongo/pull/50) Fix a bug
  in read preference handling (Kevin Funk).
- [#46](https://github.com/dcrosta/flask-pymongo/issues/46) Cannot
  use multiple replicaset instances which run on different ports (Mark
  Unsworth).
- [#30](https://github.com/dcrosta/flask-pymongo/issues/30)
  ConfiguationError with MONGO_READ_PREFERENCE (Mark Unsworth).

## 0.3.0: July 4, 2013

- This is a minor version bump which introduces backwards breaking
  changes! Please read these change notes carefully.
- Removed read preference constants from Flask-PyMongo; to set a read
  preference, use the string name or import constants directly from
  `pymongo.read_preferences.ReadPreference`.
- [#22 (partial)](https://github.com/dcrosta/flask-pymongo/pull/22)
  Add support for `MONGO_SOCKET_TIMEOUT_MS` and
  `MONGO_CONNECT_TIMEOUT_MS` options (ultrabug).
- [#27 (partial)](https://github.com/dcrosta/flask-pymongo/pull/27)
  Make Flask-PyMongo compatible with Python 3 (Vizzy).

## 0.2.1: December 22, 2012

- [#19](https://github.com/dcrosta/flask-pymongo/pull/19) Added
  `MONGO_DOCUMENT_CLASS` config option (jeverling).

## 0.2.0: December 15, 2012

- This is a minor version bump which may introduce backwards breaking
  changes! Please read these change notes carefully.
- [#17](https://github.com/dcrosta/flask-pymongo/pull/17) Now using
  PyMongo 2.4's `MongoClient` and `MongoReplicaSetClient` objects
  instead of `Connection` and `ReplicaSetConnection` classes
  (tang0th).
- [#17](https://github.com/dcrosta/flask-pymongo/pull/17) Now
  requiring at least PyMongo version 2.4 (tang0th).
- [#17](https://github.com/dcrosta/flask-pymongo/pull/17) The wrapper
  class `flask_pymongo.wrappers.Connection` is renamed to
  `flask_pymongo.wrappers.MongoClient` (tang0th).
- [#17](https://github.com/dcrosta/flask-pymongo/pull/17) The wrapper
  class `flask_pymongo.wrappers.ReplicaSetConnection` is renamed to
  `flask_pymongo.wrappers.MongoReplicaSetClient` (tang0th).
- [#18](https://github.com/dcrosta/flask-pymongo/issues/18)
  `MONGO_AUTO_START_REQUEST` now defaults to `False` when connecting
  using a URI.

## 0.1.4: December 15, 2012

- [#15](https://github.com/dcrosta/flask-pymongo/pull/15) Added
  support for `MONGO_MAX_POOL_SIZE` (Fabrice Aneche)

## 0.1.3: September 22, 2012

- Added support for configuration from MongoDB URI.

## 0.1.2: June 18, 2012

- Updated wiki example application
- [#14](https://github.com/dcrosta/flask-pymongo/issues/14) Added
  examples and docs to PyPI package.

## 0.1.1: May 26, 2012

- Added support for PyMongo 2.2's "auto start request" feature, by way
  of the `MONGO_AUTO_START_REQUEST` configuration flag.
- [#13](https://github.com/dcrosta/flask-pymongo/pull/13) Added
  BSONObjectIdConverter (Christoph Herr)
- [#12](https://github.com/dcrosta/flask-pymongo/pull/12) Corrected
  documentation typo (Thor Adam)

## 0.1: December 21, 2011

- Initial Release
