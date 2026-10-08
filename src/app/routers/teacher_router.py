from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_teacher_service
from src.app.models.user import User
from src.app.schemas.teacher_sch import CreateTeacherSch, GetTeacherDetailsSch, UpdateTeacherSch
from src.app.serviceImpl.auth_service_impl import get_admin_or_operator
from src.app.services.teacher_service import TeacherService
from src.app.shared.response import Response, PaginationResponse

teacher_router = APIRouter()


@teacher_router.post("", response_model=Response[int], name="Create Teacher")
async def create_teacher(sch: CreateTeacherSch, session: AsyncSession = Depends(get_db),
                         user: User = Depends(get_admin_or_operator),
                         service: TeacherService = Depends(get_teacher_service)):
    return Response[int](body=await service.create_teacher(sch, session))

@teacher_router.put("", response_model=Response[str], name="Update Teacher")
async def update_teacher(sch: UpdateTeacherSch, session: AsyncSession = Depends(get_db),
                         user: User = Depends(get_admin_or_operator),
                         service: TeacherService = Depends(get_teacher_service)):
    return Response[str](body=await service.update_teacher(sch, session))

@teacher_router.get("/get_all_teacher", response_model=PaginationResponse[GetTeacherDetailsSch], name="Get all Teacher Details")
async def get_all_teacher(search: str | None = None,
                          institution_id: int | None = None,
                          page: int = Query(1,ge=1),
                          size: int = Query(10,ge=1, le=100),
                          session: AsyncSession = Depends(get_db),
                          user: User = Depends(get_admin_or_operator),
                          service: TeacherService = Depends(get_teacher_service)):
    return await service.get_all_teacher(user, search, institution_id, page, size, session)

@teacher_router.get("/{teacher_id}", response_model=Response[GetTeacherDetailsSch], name="Get Teacher Details by id")
async def get_teacher_by_id(teacher_id : int, session: AsyncSession = Depends(get_db),
                            user: User = Depends(get_admin_or_operator),
                            service: TeacherService = Depends(get_teacher_service)):
    return Response[GetTeacherDetailsSch](body= await service.get_teacher_by_id(teacher_id, session))

@teacher_router.delete("/{teacher_id}", response_model=Response[str], name="Delete Teacher")
async def delete_teacher(teacher_id : int, session: AsyncSession = Depends(get_db),
                         user: User = Depends(get_admin_or_operator),
                         service: TeacherService = Depends(get_teacher_service)):
    return Response[str](body= await service.delete_teacher(teacher_id, session))
