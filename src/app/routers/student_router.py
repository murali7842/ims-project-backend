from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_student_service
from src.app.models.user import User
from src.app.schemas.student_sch import CreateStudentSch
from src.app.serviceImpl.auth_service_impl import get_admin_or_operator
from src.app.services.student_service import StudentService
from src.app.shared.response import Response

student_router = APIRouter()


@student_router.post("", response_model=Response[int], name="Create student")
async def create_student(sch: CreateStudentSch, session: AsyncSession = Depends(get_db),
                        user: User = Depends(get_admin_or_operator),
                         service: StudentService = Depends(get_student_service)):
    return Response[int](body=await service.create_student(sch, session))

