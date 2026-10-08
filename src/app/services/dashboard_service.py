from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.user import User
from src.app.schemas.dashboard_sch import DashboardSummarySch, RoleCountSch, RecentInstitutionSch, RecentUserSch
from src.app.schemas.institution_sch import InstitutionDropDown


class DashboardService(ABC):

    @abstractmethod
    async def get_institution_dropdown(self, user: User, db: AsyncSession) -> list[InstitutionDropDown]:
        pass

    @abstractmethod
    async def get_summary(self, user: User, institution_id: int | None, db: AsyncSession) -> DashboardSummarySch:
        pass

    @abstractmethod
    async def get_users_by_role(self, user: User, institution_id: int | None, year: int | None, month: int | None,
                                db: AsyncSession) -> list[RoleCountSch]:
        pass

    @abstractmethod
    async def get_recent_institutions(self, user: User, institution_id: int | None, limit: int,
                                      db: AsyncSession) -> list[RecentInstitutionSch]:
        pass

    @abstractmethod
    async def get_recent_users(self, user: User, institution_id: int | None, limit: int,
                               db: AsyncSession) -> list[RecentUserSch]:
        pass
