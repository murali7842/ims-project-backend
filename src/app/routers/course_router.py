from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_course_service
from src.app.models.user import User
from src.app.schemas.course_sch import CreateCourseSch, GetCourseSch
from src.app.serviceImpl.auth_service_impl import get_admin_or_operator
from src.app.services.course_service import CourseService
from src.app.shared.response import Response

course_router = APIRouter()


@course_router.post("", response_model=Response[int], name="Create Course")
async def create_course(sch: CreateCourseSch, session: AsyncSession = Depends(get_db),
                        user: User = Depends(get_admin_or_operator),
                         service: CourseService = Depends(get_course_service)):
    return Response[int](body=await service.create_course(sch, session))

@course_router.get("/{course_id}", response_model=Response[GetCourseSch], name="Get Course Details By ID")
async def get_course_by_id(course_id : int,
                           session: AsyncSession = Depends(get_db),
                           user: User = Depends(get_admin_or_operator),
                         service: CourseService = Depends(get_course_service)):
    return Response[GetCourseSch](body=await service.get_course_by_id(course_id,session))
