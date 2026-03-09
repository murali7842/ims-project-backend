from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.exception import errors
from src.app.models.institution import Institution
from src.app.repositories.institution_repo import InstitutionRepo
from src.app.schemas.institution_sch import InstitutionCreateSch, InstitutionSch
from src.app.services.institution_service import InstitutionService


class InstitutionServiceImpl(InstitutionService):

    def __init__(self,
                 institution_repo: InstitutionRepo,
                 ):
        super().__init__()
        self.institution_repo = institution_repo

    async def create_institution(self, sch: InstitutionCreateSch, db: AsyncSession) -> InstitutionSch:

        institution_exists = await self.institution_repo.is_institution_exists(sch.name,db)
        if institution_exists:
            raise errors.HTTPError(code=400, msg="institution with this name already exists")
        institution = Institution()
        sch.fill_entity(institution)
        institution = await self.institution_repo.save(institution, db)
        return InstitutionSch.from_entity(institution)
