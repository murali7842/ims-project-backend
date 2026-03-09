#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, TypeVar

import msgspec
from sqlalchemy import Row, RowMapping
from starlette.responses import JSONResponse

RowData = Row | RowMapping | Any

R = TypeVar('R', bound=RowData)


class MsgSpecJSONResponse(JSONResponse):
    """
    JSON response using the high-performance msgspec library to serialize data to JSON.
    """

    def render(self, content: Any) -> bytes:
        return msgspec.json.encode(content)
