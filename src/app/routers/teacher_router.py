from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_teacher_service
from src.app.models.user import User
from src.app.schemas.teacher_sch import CreateTeacherSch
from src.app.serviceImpl.auth_service_impl import get_admin_or_operator
from src.app.services.teacher_service import TeacherService
from src.app.shared.response import Response

teacher_router = APIRouter()


@teacher_router.post("", response_model=Response[int], name="Create Teacher")
async def create_teacher(sch: CreateTeacherSch, session: AsyncSession = Depends(get_db),
                         user: User = Depends(get_admin_or_operator),
                         service: TeacherService = Depends(get_teacher_service)):
    return Response[int](body=await service.create_teacher(sch, session))