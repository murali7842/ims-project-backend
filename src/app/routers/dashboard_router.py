from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_dashboard_service
from src.app.models.user import User
from src.app.schemas.dashboard_sch import DashboardSummarySch, RoleCountSch, RecentInstitutionSch, RecentUserSch
from src.app.schemas.institution_sch import InstitutionDropDown
from src.app.serviceImpl.auth_service_impl import get_admin_or_operator
from src.app.services.dashboard_service import DashboardService
from src.app.shared.response import Response

dashboard_router = APIRouter()

# institution_id: Admin -> optional (None = all institutions), Operator -> ignored, always own institution


@dashboard_router.get("/institutions", response_model=Response[list[InstitutionDropDown]],
                      name="Dashboard Institution Filter Dropdown")
async def get_institution_dropdown(user: User = Depends(get_admin_or_operator),
                                   service: DashboardService = Depends(get_dashboard_service),
                                   db: AsyncSession = Depends(get_db)):
    return Response[list[InstitutionDropDown]](body=await service.get_institution_dropdown(user, db))

@dashboard_router.get("/summary", response_model=Response[DashboardSummarySch], name="Dashboard Summary Cards")
async def get_summary(institution_id: int | None = None,
                      user: User = Depends(get_admin_or_operator),
                      service: DashboardService = Depends(get_dashboard_service),
                      db: AsyncSession = Depends(get_db)):
    return Response[DashboardSummarySch](body=await service.get_summary(user, institution_id, db))

@dashboard_router.get("/users_by_role", response_model=Response[list[RoleCountSch]], name="Users by Role")
async def get_users_by_role(institution_id: int | None = None,
                            year: int | None = Query(None, ge=2000, le=9999),
                            month: int | None = Query(None, ge=1, le=12),
                            user: User = Depends(get_admin_or_operator),
                            service: DashboardService = Depends(get_dashboard_service),
                            db: AsyncSession = Depends(get_db)):
    return Response[list[RoleCountSch]](body=await service.get_users_by_role(user, institution_id, year, month, db))

@dashboard_router.get("/recent_institutions", response_model=Response[list[RecentInstitutionSch]],
                      name="Recent Institutions")
async def get_recent_institutions(institution_id: int | None = None,
                                  limit: int = Query(5, ge=1, le=50),
                                  user: User = Depends(get_admin_or_operator),
                                  service: DashboardService = Depends(get_dashboard_service),
                                  db: AsyncSession = Depends(get_db)):
    return Response[list[RecentInstitutionSch]](
        body=await service.get_recent_institutions(user, institution_id, limit, db))

@dashboard_router.get("/recent_users", response_model=Response[list[RecentUserSch]], name="Recent Users")
async def get_recent_users(institution_id: int | None = None,
                           limit: int = Query(5, ge=1, le=50),
                           user: User = Depends(get_admin_or_operator),
                           service: DashboardService = Depends(get_dashboard_service),
                           db: AsyncSession = Depends(get_db)):
    return Response[list[RecentUserSch]](body=await service.get_recent_users(user, institution_id, limit, db))
