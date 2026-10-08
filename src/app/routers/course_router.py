from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_course_service
from src.app.models.enum import SortOrder
from src.app.models.user import User
from src.app.schemas.course_sch import CreateCourseSch, GetCourseSch, UpdateCourseSch, CourseSortBy
from src.app.serviceImpl.auth_service_impl import get_admin_or_operator
from src.app.services.course_service import CourseService
from src.app.shared.response import Response, PaginationResponse

course_router = APIRouter()


@course_router.post("", response_model=Response[int], name="Create Course")
async def create_course(sch: CreateCourseSch, session: AsyncSession = Depends(get_db),
                        user: User = Depends(get_admin_or_operator),
                        service: CourseService = Depends(get_course_service)):
    return Response[int](body=await service.create_course(sch, session))

@course_router.get("/get_all_courses", response_model=PaginationResponse[GetCourseSch], name="Get all Courses")
async def get_all_courses(search: str | None = None,
                          institution_id: int | None = None,
                          sort_by: CourseSortBy = CourseSortBy.ID,
                          sort_order: SortOrder = SortOrder.DESC,
                          page: int = Query(1, ge=1),
                          size: int = Query(10, ge=1, le=100),
                          session: AsyncSession = Depends(get_db),
                          user: User = Depends(get_admin_or_operator),
                          service: CourseService = Depends(get_course_service)):
    return await service.get_all_courses(user, search, institution_id, sort_by, sort_order, page, size, session)

@course_router.get("/{course_id}", response_model=Response[GetCourseSch], name="Get Course Details By ID")
async def get_course_by_id(course_id: int,
                           session: AsyncSession = Depends(get_db),
                           user: User = Depends(get_admin_or_operator),
                           service: CourseService = Depends(get_course_service)):
    return Response[GetCourseSch](body=await service.get_course_by_id(course_id, session))

@course_router.patch("/{course_id}", response_model=Response[str], name="Update Course")
async def update_course(course_id: int, sch: UpdateCourseSch,
                        session: AsyncSession = Depends(get_db),
                        user: User = Depends(get_admin_or_operator),
                        service: CourseService = Depends(get_course_service)):
    return Response[str](body=await service.update_course(course_id, sch, session))

@course_router.delete("/{course_id}", response_model=Response[str], name="Delete Course")
async def delete_course(course_id: int,
                        session: AsyncSession = Depends(get_db),
                        user: User = Depends(get_admin_or_operator),
                        service: CourseService = Depends(get_course_service)):
    return Response[str](body=await service.delete_course(course_id, session))
