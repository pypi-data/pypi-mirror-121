#!/usr/bin/env python
# -- coding: utf-8 --
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging

from django.http import HttpResponseBadRequest, JsonResponse
from django.utils.functional import wraps
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.decorators import api_view

from .query.engines import Executor
from .query.exceptions import QueryError, QueryExpired

LOG = logging.getLogger(__name__)


def api_error_handler(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        response = {}

        try:
            return f(*args, **kwargs)
        except QueryExpired:
            response["query_status"] = {"status": "expired"}
            response["status"] = 0
        except QueryError as e:
            LOG.exception("Error running %s" % f.__name__)
            response["status"] = 1
            response["message"] = e.message
        finally:
            if response:
                return JsonResponse(response)

    return wrapper


@extend_schema(
    description="Sync SQL statement execution",
    request={"application/json": OpenApiTypes.OBJECT},
    responses=OpenApiTypes.STR,
)
@api_view(["POST"])
def query(request, dialect=None):
    statement = request.data.get("statement")

    if not statement:
        return HttpResponseBadRequest()

    interpreter = _get_interpreter(request.data)

    data = Executor(username=request.user, interpreter=interpreter).query(
        statement=statement
    )

    return JsonResponse(data)


@api_view(["POST"])
def create_session(request):
    return JsonResponse(
        {"status": 0, "session": {"type": "1", "id": None, "properties": []}}
    )


@extend_schema(
    description="Async SQL statement execution",
    request=OpenApiTypes.STR,
    responses=OpenApiTypes.STR,
)
@api_view(["POST"])
@api_error_handler
def execute(request, dialect=None):
    statement = (
        request.data.get("statement")
        or json.loads(request.data.get("executable"))["statement"]
    )
    interpreter = _get_interpreter(request.data)

    if not statement:
        return HttpResponseBadRequest()

    handle = Executor(username=request.user, interpreter=interpreter).execute(
        statement=statement
    )

    return JsonResponse(
        {
            "status": 0,
            "handle": handle,
            "history_id": 1396,  # To push down to Engine but needed in current js
            "history_uuid": handle["guid"],  # Same
        }
    )


@api_view(["POST"])
@api_error_handler
def check_status(request):
    query_id = request.data.get("query_id")
    if not query_id:
        query_id = request.data.get("operationId")

    interpreter = _get_interpreter(query_id)

    data = Executor(username=request.user, interpreter=interpreter).check_status(
        query_id=query_id
    )

    # Note: {"status": "available", "has_result_set": true}
    return JsonResponse({"status": 0, "query_status": data})


@api_view(["POST"])
@api_error_handler
def fetch_result_data(request):
    query_id = request.data.get("operationId")
    rows = json.loads(request.data.get("rows", "100"))
    start_over = json.loads(request.data.get("startOver", "false"))

    interpreter = _get_interpreter(query_id)

    response = Executor(username=request.user, interpreter=interpreter).fetch_result(
        query_id=query_id, rows=rows, start_over=start_over
    )

    return JsonResponse(
        {
            "result": response,
            "status": 0,
        }
    )


@api_view(["POST"])
@api_error_handler
def get_logs(request):
    return JsonResponse(
        {"status": 0, "logs": "", "progress": 50, "jobs": [], "isFullLogs": True}
    )


@api_view(["POST"])
@api_error_handler
def cancel(request):
    return JsonResponse({})


@api_view(["POST"])
@api_error_handler
def close(request):
    return JsonResponse({})


@api_view(["POST"])
@api_error_handler
def close_session(request):
    return JsonResponse({})


@api_view(["POST"])
@api_error_handler
def autocomplete(request, database=None, table=None, column=None, nested=None):
    print(request.data)
    print(request.POST)

    interpreter = _get_interpreter(request.data)

    data = Executor(username=request.user, interpreter=interpreter).autocomplete(
        database=database, table=table, column=column, nested=nested
    )

    return JsonResponse(data)


def _get_interpreter(query_id):
    # TODO
    # From query_id get connector_id and so get interpreter
    # connector_id = ...

    interpreter = {
        "options": {
            "url": "sqlite:///db-demo.sqlite3"  # Dev server only (single threading)
            # "url": "mysql://hue:hue@localhost:3306/hue"
        },
        "name": "mysql",
        "dialect_properties": {},
        "dialect": "mysql",
    }

    return interpreter


# API specs
# Operation: https://swagger.io/specification/#operation-object
# Some possibilities, obviously going more manual if we don't have models. Can be case per case depending on API popularity.
# - Manual text docs like on current API docs
# - Reuse/Create a DRF serializer
# - Manual request to text and example object
# - Manual request body (and response)
@extend_schema(
    description="Minimal API for submitting an SQL statement synchronously",
    request={"application/json": OpenApiTypes.OBJECT},
    responses=OpenApiTypes.STR,
    examples=[
        OpenApiExample(
            name="SELECT 1, 2, 3",
            value={"statement": "SELECT 1, 2, 3"},
        )
    ],
    # Full override, all manual
    # https://github.com/tfranzel/drf-spectacular/issues/279
    # https://github.com/tfranzel/drf-spectacular/blob/6f12e8d9310ca2aaa833a1167d0d5f7795e2d635/tests/test_extend_schema.py#L160-L186
    # Note: seems to lose Parameters when set?
    operation={
        "operationId": "manual_endpoint",
        "tags": ["editor"],
        # https://swagger.io/specification/#request-body-object
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "examples": {
                        "1, 2, 3": {
                            "summary": "List of numbers",
                            "value": ["1", "2", "3"],
                        },
                    },
                    # "schema": {
                    #     "type": "object",
                    #     "properties": {"statement": {"type": "string"}},
                    #     "example": {"statement": "SELECT 1, 2, 3"}
                    # },
                }
            },
        },
    },
)
@api_view(["POST"])
def hello(request, message=None):
    print(request.data)
    print(request.POST)

    return JsonResponse({"data": request.data, "message": message})
