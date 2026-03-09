from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.common.constant.msg_code import APIMsgCode
from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_user_service
from src.app.schemas.user_sch import UserRegSch
from src.app.services.user_service import UserService
from src.app.shared.response import Response

user_router = APIRouter()


@user_router.post("/register", response_model=Response[int], name="User Registration")
async def reg_user(sch: UserRegSch, session: AsyncSession = Depends(get_db), service: UserService = Depends(get_user_service)):
    return Response[int](body=await service.reg_user(sch, session))

