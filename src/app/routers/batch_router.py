from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_batch_service
from src.app.models.enum import SortOrder
from src.app.models.user import User
from src.app.schemas.batch_sch import CreateBatchSch, GetBatchSch, UpdateBatchSch, BatchSortBy
from src.app.serviceImpl.auth_service_impl import get_admin_or_operator
from src.app.services.batch_service import BatchService
from src.app.shared.response import Response, PaginationResponse

batch_router = APIRouter()


@batch_router.post("", response_model=Response[int], name="Create batch")
async def create_batch(sch: CreateBatchSch, session: AsyncSession = Depends(get_db),
                       user: User = Depends(get_admin_or_operator),
                       service: BatchService = Depends(get_batch_service)):
    return Response[int](body=await service.create_batch(sch, session))

@batch_router.get("/get_all_batches", response_model=PaginationResponse[GetBatchSch], name="Get all Batches")
async def get_all_batches(search: str | None = None,
                          sort_by: BatchSortBy = BatchSortBy.ID,
                          sort_order: SortOrder = SortOrder.DESC,
                          page: int = Query(1, ge=1),
                          size: int = Query(10, ge=1, le=100),
                          session: AsyncSession = Depends(get_db),
                          user: User = Depends(get_admin_or_operator),
                          service: BatchService = Depends(get_batch_service)):
    return await service.get_all_batches(search, sort_by, sort_order, page, size, session)

@batch_router.get("/{batch_id}", response_model=Response[GetBatchSch], name="Get Batch Details By ID")
async def get_batch_by_id(batch_id: int,
                          session: AsyncSession = Depends(get_db),
                          user: User = Depends(get_admin_or_operator),
                          service: BatchService = Depends(get_batch_service)):
    return Response[GetBatchSch](body=await service.get_batch_by_id(batch_id, session))

@batch_router.patch("/{batch_id}", response_model=Response[str], name="Update Batch")
async def update_batch(batch_id: int, sch: UpdateBatchSch,
                       session: AsyncSession = Depends(get_db),
                       user: User = Depends(get_admin_or_operator),
                       service: BatchService = Depends(get_batch_service)):
    return Response[str](body=await service.update_batch(batch_id, sch, session))

@batch_router.delete("/{batch_id}", response_model=Response[str], name="Delete Batch")
async def delete_batch(batch_id: int,
                       session: AsyncSession = Depends(get_db),
                       user: User = Depends(get_admin_or_operator),
                       service: BatchService = Depends(get_batch_service)):
    return Response[str](body=await service.delete_batch(batch_id, session))
