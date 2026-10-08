from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.exception import errors
from src.app.models.enum import UserRole
from src.app.models.user import User
from src.app.repositories.dashboard_repo import DashboardRepo
from src.app.schemas.dashboard_sch import DashboardSummarySch, RoleCountSch, RecentInstitutionSch, RecentUserSch
from src.app.schemas.institution_sch import InstitutionDropDown
from src.app.services.dashboard_service import DashboardService


class DashboardServiceImpl(DashboardService):

    def __init__(self,
                 dashboard_repo: DashboardRepo,
                 ):
        super().__init__()
        self.dashboard_repo = dashboard_repo

    async def get_institution_dropdown(self, user: User, db: AsyncSession) -> list[InstitutionDropDown]:
        institution_id = self._resolve_institution_id(user, None)
        institutions = await self.dashboard_repo.get_institution_dropdown(institution_id, db)
        return [InstitutionDropDown(id=institution.id, name=institution.name) for institution in institutions]

    async def get_summary(self, user: User, institution_id: int | None, db: AsyncSession) -> DashboardSummarySch:
        institution_id = self._resolve_institution_id(user, institution_id)
        counts = await self.dashboard_repo.get_summary_counts(institution_id, db)
        return DashboardSummarySch(**counts)

    async def get_users_by_role(self, user: User, institution_id: int | None, year: int | None, month: int | None,
                                db: AsyncSession) -> list[RoleCountSch]:
        institution_id = self._resolve_institution_id(user, institution_id)
        start, end = self._get_date_range(year, month)
        rows = await self.dashboard_repo.get_users_count_by_role(institution_id, start, end, db)

        # every role is returned (0 when there is no data) so the chart always shows all bars
        role_counts = {role: 0 for role in UserRole}
        for role, count in rows:
            role_counts[UserRole(role)] += count

        return [RoleCountSch(role=role, count=count) for role, count in role_counts.items()]

    async def get_recent_institutions(self, user: User, institution_id: int | None, limit: int,
                                      db: AsyncSession) -> list[RecentInstitutionSch]:
        institution_id = self._resolve_institution_id(user, institution_id)
        institutions = await self.dashboard_repo.get_recent_institutions(institution_id, limit, db)
        return [RecentInstitutionSch.from_entity(institution) for institution in institutions]

    async def get_recent_users(self, user: User, institution_id: int | None, limit: int,
                               db: AsyncSession) -> list[RecentUserSch]:
        institution_id = self._resolve_institution_id(user, institution_id)
        users = await self.dashboard_repo.get_recent_users(institution_id, limit, db)
        return [RecentUserSch(id=user.id, name=user.name, email=user.email, role=user.role,
                              created_at=user.created_at) for user in users]

    @staticmethod
    def _resolve_institution_id(user: User, institution_id: int | None) -> int | None:
        """Admin can view all institutions or filter by one; operator is always scoped to own institution"""
        if user.role == UserRole.ADMIN:
            return institution_id

        if user.institution_id is None:
            raise errors.HTTPError(code=403, msg="Operator is not linked to any institution")
        return user.institution_id

    @staticmethod
    def _get_date_range(year: int | None, month: int | None) -> tuple[datetime | None, datetime | None]:
        """Convert year/month filters into a [start, end) datetime range"""
        if year is None:
            if month is not None:
                raise errors.HTTPError(code=400, msg="year is required when month is given")
            return None, None

        if month is None:
            return (datetime(year, 1, 1, tzinfo=timezone.utc),
                    datetime(year + 1, 1, 1, tzinfo=timezone.utc))

        start = datetime(year, month, 1, tzinfo=timezone.utc)
        end = datetime(year + 1, 1, 1, tzinfo=timezone.utc) if month == 12 \
            else datetime(year, month + 1, 1, tzinfo=timezone.utc)
        return start, end
