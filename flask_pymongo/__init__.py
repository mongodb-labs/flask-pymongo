# Copyright (c) 2011-2017, Dan Crosta
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


__all__ = ("PyMongo", "ASCENDING", "DESCENDING")

from functools import partial
from mimetypes import guess_type

from flask import abort, current_app, request
from gridfs import GridFS, NoFile
from pymongo import uri_parser
from werkzeug.wsgi import wrap_file
import pymongo
# DriverInfo was added in PyMongo 3.7
try:
    from pymongo.driver_info import DriverInfo
except ImportError:
    DriverInfo = None

from flask_pymongo._version import __version__
from flask_pymongo.helpers import BSONObjectIdConverter, JSONEncoder
from flask_pymongo.wrappers import MongoClient

DESCENDING = pymongo.DESCENDING
"""Descending sort order."""

ASCENDING = pymongo.ASCENDING
"""Ascending sort order."""


class PyMongo(object):

    """Manages MongoDB connections for your Flask app.

    PyMongo objects provide access to the MongoDB server via the :attr:`db`
    and :attr:`cx` attributes. You must either pass the :class:`~flask.Flask`
    app to the constructor, or call :meth:`init_app`.

    PyMongo accepts a MongoDB URI via the ``MONGO_URI`` Flask configuration
    variable, or as an argument to the constructor or ``init_app``. See
    :meth:`init_app` for more detail.

    """

    def __init__(self, app=None, uri=None, json_options=None, *args, **kwargs):
        self.cx = None
        self.db = None
        self._json_encoder = partial(JSONEncoder, json_options=json_options)

        if app is not None:
            self.init_app(app, uri, *args, **kwargs)

    def init_app(self, app, uri=None, *args, **kwargs):
        """Initialize this :class:`PyMongo` for use.

        Configure a :class:`~pymongo.mongo_client.MongoClient`
        in the following scenarios:

        1. If ``uri`` is not ``None``, pass the ``uri`` and any positional
           or keyword arguments to :class:`~pymongo.mongo_client.MongoClient`
        2. If ``uri`` is ``None``, and a Flask config variable named
           ``MONGO_URI`` exists, use that as the ``uri`` as above.

        The caller is responsible for ensuring that additional positional
        and keyword arguments result in a valid call.

        .. versionchanged:: 2.2

           The ``uri`` is no longer required to contain a database name. If it
           does not, then the :attr:`db` attribute will be ``None``.

        .. versionchanged:: 2.0

           Flask-PyMongo no longer accepts many of the configuration variables
           it did in previous versions. You must now use a MongoDB URI to
           configure Flask-PyMongo.

        """
        if uri is None:
            uri = app.config.get("MONGO_URI", None)
        if uri is not None:
            args = tuple([uri] + list(args))
        else:
            raise ValueError(
                "You must specify a URI or set the MONGO_URI Flask config variable",
            )

        parsed_uri = uri_parser.parse_uri(uri)
        database_name = parsed_uri["database"]

        # Try to delay connecting, in case the app is loaded before forking, per
        # http://api.mongodb.com/python/current/faq.html#is-pymongo-fork-safe
        kwargs.setdefault("connect", False)
        if DriverInfo is not None:
            kwargs.setdefault("driver", DriverInfo("Flask-PyMongo", __version__))

        self.cx = MongoClient(*args, **kwargs)
        if database_name:
            self.db = self.cx[database_name]

        app.url_map.converters["ObjectId"] = BSONObjectIdConverter
        app.json_encoder = self._json_encoder

    # view helpers
    def send_file(self, filename, base="fs", version=-1, cache_for=31536000):
        """Respond with a file from GridFS.

        Returns an instance of the :attr:`~flask.Flask.response_class`
        containing the named file, and implement conditional GET semantics
        (using :meth:`~werkzeug.wrappers.ETagResponseMixin.make_conditional`).

        .. code-block:: python

            @app.route("/uploads/<path:filename>")
            def get_upload(filename):
                return mongo.send_file(filename)

        :param str filename: the filename of the file to return
        :param str base: the base name of the GridFS collections to use
        :param bool version: if positive, return the Nth revision of the file
           identified by filename; if negative, return the Nth most recent
           revision. If no such version exists, return with HTTP status 404.
        :param int cache_for: number of seconds that browsers should be
           instructed to cache responses
        """
        if not isinstance(base, str):
            raise TypeError("'base' must be string or unicode")
        if not isinstance(version, int):
            raise TypeError("'version' must be an integer")
        if not isinstance(cache_for, int):
            raise TypeError("'cache_for' must be an integer")

        storage = GridFS(self.db, base)

        try:
            fileobj = storage.get_version(filename=filename, version=version)
        except NoFile:
            abort(404)

        # mostly copied from flask/helpers.py, with
        # modifications for GridFS
        data = wrap_file(request.environ, fileobj, buffer_size=1024 * 255)
        response = current_app.response_class(
            data,
            mimetype=fileobj.content_type,
            direct_passthrough=True,
        )
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        response.content_length = fileobj.length
        response.last_modified = fileobj.upload_date
        response.set_etag(fileobj.md5)
        response.cache_control.max_age = cache_for
        response.cache_control.public = True
        response.make_conditional(request)
        return response

    def save_file(self, filename, fileobj, base="fs", content_type=None, **kwargs):
        """Save a file-like object to GridFS using the given filename.

        .. code-block:: python

            @app.route("/uploads/<path:filename>", methods=["POST"])
            def save_upload(filename):
                mongo.save_file(filename, request.files["file"])
                return redirect(url_for("get_upload", filename=filename))

        :param str filename: the filename of the file to return
        :param file fileobj: the file-like object to save
        :param str base: base the base name of the GridFS collections to use
        :param str content_type: the MIME content-type of the file. If
           ``None``, the content-type is guessed from the filename using
           :func:`~mimetypes.guess_type`
        :param kwargs: extra attributes to be stored in the file's document,
           passed directly to :meth:`gridfs.GridFS.put`
        """
        if not isinstance(base, str):
            raise TypeError("'base' must be string or unicode")
        if not (hasattr(fileobj, "read") and callable(fileobj.read)):
            raise TypeError("'fileobj' must have read() method")

        if content_type is None:
            content_type, _ = guess_type(filename)

        storage = GridFS(self.db, base)
        id = storage.put(fileobj, filename=filename, content_type=content_type, **kwargs)
        return id
