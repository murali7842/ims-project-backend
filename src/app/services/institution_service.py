from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.enum import SortOrder
from src.app.schemas.institution_sch import InstitutionCreateSch, InstitutionSch, InstitutionUpdateSch, \
    InstitutionSortBy
from src.app.shared.response import PaginationResponse


class InstitutionService(ABC):

    @abstractmethod
    async def create_institution(self, sch: InstitutionCreateSch, db: AsyncSession) -> InstitutionSch:
        pass

    @abstractmethod
    async def get_institution_by_id(self, institution_id: int, db: AsyncSession) -> InstitutionSch:
        pass

    @abstractmethod
    async def get_all_institutions(self, search: str | None, sort_by: InstitutionSortBy, sort_order: SortOrder,
                                   page: int, size: int, db: AsyncSession) -> PaginationResponse[InstitutionSch]:
        pass

    @abstractmethod
    async def update_institution(self, sch: InstitutionUpdateSch, db: AsyncSession) -> str:
        pass

    @abstractmethod
    async def delete_institution(self, institution_id: int, db: AsyncSession) -> str:
        pass
