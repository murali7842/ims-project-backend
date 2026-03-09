from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_institution_service
from src.app.models.user import User
from src.app.schemas.institution_sch import InstitutionSch, InstitutionCreateSch
from src.app.serviceImpl.auth_service_impl import get_admin
from src.app.services.institution_service import InstitutionService
from src.app.shared.response import Response

institution_router = APIRouter()


@institution_router.post("", response_model=Response[InstitutionSch], name="Create Institution")
async def create_institution(sch: InstitutionCreateSch,
                           user: User = Depends(get_admin),
                           service: InstitutionService = Depends(get_institution_service),
                           db: AsyncSession = Depends(get_db)):
    return Response[InstitutionSch](body=await service.create_institution(sch, db))