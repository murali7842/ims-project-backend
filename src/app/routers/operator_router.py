from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_operator_service
from src.app.models.user import User
from src.app.schemas.operator_sch import CreateOperatorSch
from src.app.serviceImpl.auth_service_impl import get_admin
from src.app.services.operator_service import OperatorService
from src.app.shared.response import Response

operator_router = APIRouter()


@operator_router.post("", response_model=Response[int], name="Create Operator")
async def reg_user(sch: CreateOperatorSch, session: AsyncSession = Depends(get_db),
                   user: User = Depends(get_admin),
                   service: OperatorService = Depends(get_operator_service)):
    return Response[int](body=await service.create_operator(sch, session))



