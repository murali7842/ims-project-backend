from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas.institution_sch import InstitutionCreateSch, InstitutionSch


class InstitutionService(ABC):

    @abstractmethod
    async def create_institution(self, sch: InstitutionCreateSch, db: AsyncSession) -> InstitutionSch:
        pass