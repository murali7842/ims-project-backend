from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.exception import errors
from src.app.models.enum import SortOrder
from src.app.models.institution import Institution
from src.app.repositories.institution_repo import InstitutionRepo
from src.app.schemas.institution_sch import InstitutionCreateSch, InstitutionSch, InstitutionUpdateSch, \
    InstitutionSortBy
from src.app.services.institution_service import InstitutionService
from src.app.shared.response import PaginationResponse


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

    async def get_institution_by_id(self, institution_id: int, db: AsyncSession) -> InstitutionSch:
        institution = await self.institution_repo.get(institution_id, db)
        if not institution:
            raise errors.HTTPError(code=404, msg=f"Institution with id {institution_id} not found!")

        return InstitutionSch.from_entity(institution)

    async def get_all_institutions(self, search: str | None, sort_by: InstitutionSortBy, sort_order: SortOrder,
                                   page: int, size: int, db: AsyncSession) -> PaginationResponse[InstitutionSch]:
        institutions, total_elements = await self.institution_repo.get_all_institutions(
            search, sort_by, sort_order, page, size, db)

        institution_list = [InstitutionSch.from_entity(institution) for institution in institutions]

        return PaginationResponse[InstitutionSch](body=institution_list).set_page_info(
            total_elements=total_elements, page=page, size=size)

    async def update_institution(self, sch: InstitutionUpdateSch, db: AsyncSession) -> str:
        institution = await self.institution_repo.get(sch.id, db)
        if not institution:
            raise errors.HTTPError(code=404, msg=f"Institution with id {sch.id} not found!")

        if await self.institution_repo.is_institution_exists(sch.name, db, exclude_id=sch.id):
            raise errors.HTTPError(code=400, msg="institution with this name already exists")

        if await self.institution_repo.exist_by_email(sch.email, db, exclude_id=sch.id):
            raise errors.HTTPError(code=400, msg="institution with this email already exists")

        sch.fill_entity(institution)
        await self.institution_repo.save(institution, db)
        return "Institution updated successfully"

    async def delete_institution(self, institution_id: int, db: AsyncSession) -> str:
        institution = await self.institution_repo.get(institution_id, db)
        if not institution:
            raise errors.HTTPError(code=404, msg=f"Institution with id {institution_id} not found!")

        await self.institution_repo.delete_by_id(institution_id, db)
        return "Institution deleted successfully"
