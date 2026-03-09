from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_course_service, get_batch_service
from src.app.models.user import User
from src.app.schemas.batch_sch import CreateBatchSch, GetBatchSch
from src.app.schemas.course_sch import CreateCourseSch
from src.app.serviceImpl.auth_service_impl import get_admin_or_operator
from src.app.services.batch_service import BatchService
from src.app.services.course_service import CourseService
from src.app.shared.response import Response

batch_router = APIRouter()


@batch_router.post("", response_model=Response[int], name="Create batch")
async def create_course(sch: CreateBatchSch, session: AsyncSession = Depends(get_db),
                        user: User = Depends(get_admin_or_operator),
                         service: BatchService = Depends(get_batch_service)):
    return Response[int](body=await service.create_batch(sch, session))

@batch_router.get("/{batch_id}", response_model=Response[GetBatchSch], name="Get Batch Details By ID")
async def get_batch_by_id(batch_id : int,
                           session: AsyncSession = Depends(get_db),
                           user: User = Depends(get_admin_or_operator),
                         service: BatchService = Depends(get_batch_service)):
    return Response[GetBatchSch](body=await service.get_batch_by_id(batch_id, session))