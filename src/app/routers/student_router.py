from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_student_service
from src.app.models.enum import SortOrder
from src.app.models.user import User
from src.app.schemas.student_sch import CreateStudentSch, GetStudentSch, UpdateStudentSch, StudentSortBy
from src.app.serviceImpl.auth_service_impl import get_admin_or_operator
from src.app.services.student_service import StudentService
from src.app.shared.response import Response, PaginationResponse

student_router = APIRouter()


@student_router.post("", response_model=Response[int], name="Create student")
async def create_student(sch: CreateStudentSch, session: AsyncSession = Depends(get_db),
                         user: User = Depends(get_admin_or_operator),
                         service: StudentService = Depends(get_student_service)):
    return Response[int](body=await service.create_student(sch, session))

@student_router.put("", response_model=Response[str], name="Update student")
async def update_student(sch: UpdateStudentSch, session: AsyncSession = Depends(get_db),
                         user: User = Depends(get_admin_or_operator),
                         service: StudentService = Depends(get_student_service)):
    return Response[str](body=await service.update_student(sch, session))

@student_router.get("/get_all_students", response_model=PaginationResponse[GetStudentSch],
                    name="Get all Students")
async def get_all_students(search: str | None = None,
                           course_id: int | None = None,
                           batch_id: int | None = None,
                           sort_by: StudentSortBy = StudentSortBy.ID,
                           sort_order: SortOrder = SortOrder.DESC,
                           page: int = Query(1, ge=1),
                           size: int = Query(10, ge=1, le=100),
                           session: AsyncSession = Depends(get_db),
                           user: User = Depends(get_admin_or_operator),
                           service: StudentService = Depends(get_student_service)):
    return await service.get_all_students(search, course_id, batch_id, sort_by, sort_order, page, size, session)

@student_router.get("/{student_id}", response_model=Response[GetStudentSch], name="Get Student Details By ID")
async def get_student_by_id(student_id: int, session: AsyncSession = Depends(get_db),
                            user: User = Depends(get_admin_or_operator),
                            service: StudentService = Depends(get_student_service)):
    return Response[GetStudentSch](body=await service.get_student_by_id(student_id, session))

@student_router.delete("/{student_id}", response_model=Response[str], name="Delete student")
async def delete_student(student_id: int, session: AsyncSession = Depends(get_db),
                         user: User = Depends(get_admin_or_operator),
                         service: StudentService = Depends(get_student_service)):
    return Response[str](body=await service.delete_student(student_id, session))
