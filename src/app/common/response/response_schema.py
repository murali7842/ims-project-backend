from datetime import datetime
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, ConfigDict

from src.app.common.response.response_code import CustomResponseCode, CustomResponse
from src.app.config.setting import get_setting

setting = get_setting()

T = TypeVar('T')  # Define a type variable for the data field

__all__ = ['ResponseModel', 'response_base']


class ResponseModel(BaseModel, Generic[T]):
    """Generic response model that can be parametrized with different data types."""

    model_config = ConfigDict(json_encoders={
        datetime: lambda x: x.strftime(setting.DATETIME_FORMAT)
    })

    code: int = CustomResponseCode.HTTP_200.code
    msg: str = CustomResponseCode.HTTP_200.msg
    data: Optional[T] = None


class ResponseBase:
    """
    Unified response method with generic type support

    .. tip::

        The response methods in this class will return the ResponseModel model,
        serving as a coding style guideline.

    Example:
        @router.get('/test')
        def test() -> ResponseModel[dict]:
            return await response_base.success(data={'test': 'test'})
    """

    @staticmethod
    async def __response(
            *,
            res: CustomResponseCode | CustomResponse = None,
            data: Optional[T] = None
    ) -> ResponseModel[T]:
        """
        General method for successful response

        Args:
            res: Response message
            data: Response data of type T
        Returns:
            ResponseModel parametrized with type T
        """
        return ResponseModel[T](code=res.code, msg=res.msg, data=data)

    async def success(
            self,
            *,
            res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_200,
            data: Optional[T] = None,
    ) -> ResponseModel[T]:
        return await self.__response(res=res, data=data)

    async def fail(
            self,
            *,
            res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_400,
            data: Optional[T] = None,
    ) -> ResponseModel[T]:
        return await self.__response(res=res, data=data)


response_base = ResponseBase()