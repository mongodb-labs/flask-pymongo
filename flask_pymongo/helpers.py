# Copyright (c) 2011-2019, Dan Crosta
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
from __future__ import annotations

__all__ = ("BSONObjectIdConverter", "BSONProvider")

from typing import Any

from bson import json_util
from bson.errors import InvalidId
from bson.json_util import RELAXED_JSON_OPTIONS
from bson.objectid import ObjectId
from flask import abort
from flask.json.provider import JSONProvider
from werkzeug.routing import BaseConverter


class BSONObjectIdConverter(BaseConverter):
    """A simple converter for the RESTful URL routing system of Flask.

    .. code-block:: python

        @app.route("/<ObjectId:task_id>")
        def show_task(task_id):
            task = mongo.db.tasks.find_one_or_404(task_id)
            return render_template("task.html", task=task)

    Valid object ID strings are converted into
    :class:`~bson.objectid.ObjectId` objects; invalid strings result
    in a 404 error. The converter is automatically registered by the
    initialization of :class:`~flask_pymongo.PyMongo` with keyword
    :attr:`ObjectId`.

    The :class:`~flask_pymongo.helpers.BSONObjectIdConverter` is
    automatically installed on the :class:`~flask_pymongo.PyMongo`
    instance at creation time.

    """

    def to_python(self, value: Any) -> ObjectId:
        try:
            return ObjectId(value)
        except InvalidId:
            raise abort(404) from None

    def to_url(self, value: Any) -> str:
        return str(value)


class BSONProvider(JSONProvider):
    """A JSON encoder that uses :mod:`bson.json_util` for MongoDB documents.

    .. code-block:: python

        @app.route("/cart/<ObjectId:cart_id>")
        def json_route(cart_id):
            results = mongo.db.carts.find({"_id": cart_id})
            return jsonify(results)


        # returns a Response with JSON body and application/json content-type:
        # '[{"count":12,"item":"egg"},{"count":1,"item":"apple"}]'

    Since this uses PyMongo's JSON tools, certain types may serialize
    differently than you expect. See :class:`~bson.json_util.JSONOptions`
    for details on the particular serialization that will be used.

    A :class:`~flask_pymongo.helpers.JSONProvider` is automatically
    automatically installed on the :class:`~flask_pymongo.PyMongo`
    instance at creation time, using
    :const:`~bson.json_util.RELAXED_JSON_OPTIONS`.
    """

    def __init__(self, app: Any) -> None:
        self._default_kwargs = {"json_options": RELAXED_JSON_OPTIONS}

        super().__init__(app)

    def dumps(self, obj: Any, **kwargs: Any) -> str:
        """Serialize MongoDB object types using :mod:`bson.json_util`."""
        return json_util.dumps(obj)

    def loads(self, s: str | bytes, **kwargs: Any) -> Any:
        """Deserialize MongoDB object types using :mod:`bson.json_util`."""
        return json_util.loads(s)
