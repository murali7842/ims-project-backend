from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_operator_service
from src.app.models.enum import SortOrder
from src.app.models.user import User
from src.app.schemas.operator_sch import CreateOperatorSch, GetOperatorSch, UpdateOperatorSch, OperatorSortBy
from src.app.serviceImpl.auth_service_impl import get_admin
from src.app.services.operator_service import OperatorService
from src.app.shared.response import Response, PaginationResponse

operator_router = APIRouter()


@operator_router.post("", response_model=Response[int], name="Create Operator")
async def reg_user(sch: CreateOperatorSch, session: AsyncSession = Depends(get_db),
                   user: User = Depends(get_admin),
                   service: OperatorService = Depends(get_operator_service)):
    return Response[int](body=await service.create_operator(sch, session))

@operator_router.put("", response_model=Response[str], name="Update Operator")
async def update_operator(sch: UpdateOperatorSch, session: AsyncSession = Depends(get_db),
                          user: User = Depends(get_admin),
                          service: OperatorService = Depends(get_operator_service)):
    return Response[str](body=await service.update_operator(sch, session))

@operator_router.get("/get_all_operators", response_model=PaginationResponse[GetOperatorSch],
                     name="Get all Operators")
async def get_all_operators(search: str | None = None,
                            sort_by: OperatorSortBy = OperatorSortBy.ID,
                            sort_order: SortOrder = SortOrder.DESC,
                            page: int = Query(1, ge=1),
                            size: int = Query(10, ge=1, le=100),
                            session: AsyncSession = Depends(get_db),
                            user: User = Depends(get_admin),
                            service: OperatorService = Depends(get_operator_service)):
    return await service.get_all_operators(search, sort_by, sort_order, page, size, session)

@operator_router.get("/{operator_id}", response_model=Response[GetOperatorSch], name="Get Operator Details By ID")
async def get_operator_by_id(operator_id: int, session: AsyncSession = Depends(get_db),
                             user: User = Depends(get_admin),
                             service: OperatorService = Depends(get_operator_service)):
    return Response[GetOperatorSch](body=await service.get_operator_by_id(operator_id, session))

@operator_router.delete("/{operator_id}", response_model=Response[str], name="Delete Operator")
async def delete_operator(operator_id: int, session: AsyncSession = Depends(get_db),
                          user: User = Depends(get_admin),
                          service: OperatorService = Depends(get_operator_service)):
    return Response[str](body=await service.delete_operator(operator_id, session))
