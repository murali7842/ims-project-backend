from typing import Any

from fastapi import HTTPException
from starlette.background import BackgroundTask

from src.app.common.response.response_code import CustomErrorCode, StandardResponseCode


class BaseExceptionMixin(Exception):
    code: int

    def __init__(self, *, msg: str = None, data: Any = None, background: BackgroundTask | None = None, msg_code: str | None = None):
        self.msg = msg
        self.data = data
        # The original background task: https://www.starlette.io/background/
        self.background = background
        self.msg_code = msg_code


class HTTPError(HTTPException):
    def __init__(self, *, code: int, msg: Any = None, headers: dict[str, Any] | None = None):
        super().__init__(status_code=code, detail=msg, headers=headers)


class CustomError(BaseExceptionMixin):
    def __init__(self, *, error: CustomErrorCode, data: Any = None, background: BackgroundTask | None = None):
        self.code = error.code
        self.msg = error.msg
        self.data = data
        super().__init__(msg=error.msg, data=data, background=background)


class RequestError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_400

    def __init__(self, *, msg: str = 'Bad Request', data: Any = None, background: BackgroundTask | None = None, msg_code: str | None = None):
        super().__init__(msg=msg, data=data, background=background, msg_code=msg_code)


class ForbiddenError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_403

    def __init__(self, *, msg: str = 'Forbidden', data: Any = None, background: BackgroundTask | None = None, msg_code: str | None = None):
        super().__init__(msg=msg, data=data, background=background, msg_code=msg_code)


class NotFoundError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_404

    def __init__(self, *, msg: str = 'Not Found', data: Any = None, background: BackgroundTask | None = None, msg_code: str | None = None):
        super().__init__(msg=msg, data=data, background=background, msg_code=msg_code)


class ServerError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_500

    def __init__(
            self, *, msg: str = 'Internal Server Error', data: Any = None, background: BackgroundTask | None = None
    ):
        super().__init__(msg=msg, data=data, background=background)


class GatewayError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_502

    def __init__(self, *, msg: str = 'Bad Gateway', data: Any = None, background: BackgroundTask | None = None):
        super().__init__(msg=msg, data=data, background=background)


class AuthorizationError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_401

    def __init__(self, *, msg: str = 'Permission Denied', data: Any = None, background: BackgroundTask | None = None, msg_code: str|None = None):
        super().__init__(msg=msg, data=data, background=background, msg_code=msg_code)


class TokenError(HTTPError):
    code = StandardResponseCode.HTTP_401

    def __init__(self, *, msg: str = 'Not Authenticated', headers: dict[str, Any] | None = None):
        super().__init__(code=self.code, msg=msg, headers=headers or {'WWW-Authenticate': 'Bearer'})


class ConflictError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_409

    def __init__(self, *, msg: str = 'Invalid', data: Any = None, background: BackgroundTask | None = None, msg_code: str | None = None):
        super().__init__(msg=msg, data=data, background=background, msg_code=msg_code)


