from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_institution_service
from src.app.models.enum import SortOrder
from src.app.models.user import User
from src.app.schemas.institution_sch import InstitutionSch, InstitutionCreateSch, InstitutionUpdateSch, \
    InstitutionSortBy
from src.app.serviceImpl.auth_service_impl import get_admin
from src.app.services.institution_service import InstitutionService
from src.app.shared.response import Response, PaginationResponse

institution_router = APIRouter()


@institution_router.post("", response_model=Response[InstitutionSch], name="Create Institution")
async def create_institution(sch: InstitutionCreateSch,
                           user: User = Depends(get_admin),
                           service: InstitutionService = Depends(get_institution_service),
                           db: AsyncSession = Depends(get_db)):
    return Response[InstitutionSch](body=await service.create_institution(sch, db))

@institution_router.put("", response_model=Response[str], name="Update Institution")
async def update_institution(sch: InstitutionUpdateSch,
                             user: User = Depends(get_admin),
                             service: InstitutionService = Depends(get_institution_service),
                             db: AsyncSession = Depends(get_db)):
    return Response[str](body=await service.update_institution(sch, db))

@institution_router.get("/get_all_institutions", response_model=PaginationResponse[InstitutionSch],
                        name="Get all Institutions")
async def get_all_institutions(search: str | None = None,
                               sort_by: InstitutionSortBy = InstitutionSortBy.ID,
                               sort_order: SortOrder = SortOrder.DESC,
                               page: int = Query(1, ge=1),
                               size: int = Query(10, ge=1, le=100),
                               user: User = Depends(get_admin),
                               service: InstitutionService = Depends(get_institution_service),
                               db: AsyncSession = Depends(get_db)):
    return await service.get_all_institutions(search, sort_by, sort_order, page, size, db)

@institution_router.get("/{institution_id}", response_model=Response[InstitutionSch],
                        name="Get Institution Details By ID")
async def get_institution_by_id(institution_id: int,
                                user: User = Depends(get_admin),
                                service: InstitutionService = Depends(get_institution_service),
                                db: AsyncSession = Depends(get_db)):
    return Response[InstitutionSch](body=await service.get_institution_by_id(institution_id, db))

@institution_router.delete("/{institution_id}", response_model=Response[str], name="Delete Institution")
async def delete_institution(institution_id: int,
                             user: User = Depends(get_admin),
                             service: InstitutionService = Depends(get_institution_service),
                             db: AsyncSession = Depends(get_db)):
    return Response[str](body=await service.delete_institution(institution_id, db))
