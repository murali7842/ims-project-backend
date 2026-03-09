import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic.errors import PydanticUserError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from src.app.common.constant.msg_code import APIMsgCode
from src.app.common.exception.errors import BaseExceptionMixin, AuthorizationError
from src.app.common.response.response_code import StandardResponseCode, CustomResponseCode
from src.app.common.response.response_schema import response_base
from src.app.config.setting import get_setting
from src.app.schemas.base import CUSTOM_USAGE_ERROR_MESSAGES
from src.app.utils.serializers import MsgSpecJSONResponse

log = logging.getLogger()
setting = get_setting()


def register_exception(app: FastAPI):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        msg = {
            "success": False,
            "data": {
              "fields": [str(error.get('loc')[-1]) for error in exc.errors()],
              "details": [{"type": error['type'], "field": error.get('loc')[-1], "msg": error['msg']} for error in exc.errors()]
            },
            "msg_code": APIMsgCode.INVALID_PAYLOAD,
            "msg": "Request payload has invalid value(s)"
        }
        return MsgSpecJSONResponse(status_code=StandardResponseCode.HTTP_422, content=msg)

    @app.exception_handler(AuthorizationError)
    async def auth_error_handler(request: Request, exc: AuthorizationError):
        resp = {
            "success": False,
            "msg_code": exc.msg_code,
            "msg": exc.msg
        }
        return MsgSpecJSONResponse(status_code=exc.code, content=resp)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        log.error("In http r")
        log.exception(exc)
        """


        :param request:
        :param exc:
        :return:
        """
        content = {
            'success': False,
            'code': exc.status_code,
            'msg': exc.detail,
            'data': None,
        }
        request.state.__request_http_exception__ = content
        return MsgSpecJSONResponse(
            status_code=exc.status_code,
            content=content,
            headers=exc.headers,
        )

    @app.exception_handler(PydanticUserError)
    async def pydantic_user_error_handler(request: Request, exc: PydanticUserError):
        """


        :param request:
        :param exc:
        :return:
        """
        log.exception(exc)

        return MsgSpecJSONResponse(
            status_code=StandardResponseCode.HTTP_500,
            content={
                'success': False,
                'code': StandardResponseCode.HTTP_500,
                'msg': CUSTOM_USAGE_ERROR_MESSAGES.get(exc.code),
                'data': None,
            },
        )

    @app.exception_handler(AssertionError)
    async def assertion_error_handler(request: Request, exc: AssertionError):
        """


        :param request:
        :param exc:
        :return:
        """
        log.exception(exc)

        content = {
            'success': False,
            'code': StandardResponseCode.HTTP_400,
            'msg': str(''.join(exc.args) if exc.args else exc.__doc__),
            'data': None,
        }
        return MsgSpecJSONResponse(
            status_code=StandardResponseCode.HTTP_400,
            content=content,
        )

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        log.error(f"Exception in")
        """


        :param request:
        :param exc:
        :return:
        """
        if isinstance(exc, BaseExceptionMixin):
            return MsgSpecJSONResponse(
                status_code=StandardResponseCode.HTTP_400,
                content={
                    'success': False,
                    'code': exc.code,
                    'msg': str(exc.msg),
                    'data': exc.data if exc.data else None,
                    'msg_code': exc.msg_code
                },
                background=exc.background,
            )
        else:
            import traceback

            log.error(f'Unknown exception: {exc}')
            log.error(traceback.format_exc())
            if setting.PROFILE == 'Dev':
                content = {
                    'success': False,
                    'code': 500,
                    'msg': str(exc),
                    'data': None,
                }
            else:
                res = await response_base.fail(res=CustomResponseCode.HTTP_500)
                content = res.model_dump()
            return MsgSpecJSONResponse(status_code=StandardResponseCode.HTTP_500, content=content)

    if setting.MIDDLEWARE_CORS:

        @app.exception_handler(StandardResponseCode.HTTP_500)
        async def cors_status_code_500_exception_handler(request, exc):
            """


            `Related issue <https://github.com/encode/starlette/issues/1175>`_

            :param request:
            :param exc:
            :return:
            """
            if isinstance(exc, BaseExceptionMixin):
                content = {
                    'success': False,
                    'code': exc.code,
                    'msg': exc.msg,
                    'data': exc.data,
                    'msg_code': exc.msg_code
                }
            else:
                if setting.PROFILE == 'Dev':
                    content = {
                        'success': False,
                        'code': StandardResponseCode.HTTP_500,
                        'msg': str(exc),
                        'data': None,
                    }
                else:
                    res = await response_base.fail(res=CustomResponseCode.HTTP_500)
                    content = res.model_dump()
            response = MsgSpecJSONResponse(
                status_code=exc.code if isinstance(exc, BaseExceptionMixin) else StandardResponseCode.HTTP_500,
                content=content,
                background=exc.background if isinstance(exc, BaseExceptionMixin) else None,
            )
            origin = request.headers.get('origin')
            if origin:
                cors = CORSMiddleware(
                    app=app,
                    allow_origins=['*'],
                    allow_credentials=True,
                    allow_methods=['*'],
                    allow_headers=['*'],
                )
                response.headers.update(cors.simple_headers)
                has_cookie = 'cookie' in request.headers
                if cors.allow_all_origins and has_cookie:
                    response.headers['Access-Control-Allow-Origin'] = origin
                elif not cors.allow_all_origins and cors.is_allowed_origin(origin=origin):
                    response.headers['Access-Control-Allow-Origin'] = origin
                    response.headers.add_vary_header('Origin')
            return response
