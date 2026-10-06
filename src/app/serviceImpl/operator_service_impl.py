from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.exception import errors
from src.app.config.security import get_password_hash
from src.app.models.enum import UserRole, SortOrder
from src.app.models.user import User
from src.app.repositories.institution_repo import InstitutionRepo
from src.app.repositories.operator_repo import OperatorRepo
from src.app.repositories.user_repo import UserRepo
from src.app.schemas.operator_sch import CreateOperatorSch, GetOperatorSch, UpdateOperatorSch, OperatorSortBy
from src.app.services.operator_service import OperatorService
from src.app.shared.response import PaginationResponse


class OperatorServiceImpl(OperatorService):

    def __init__(self,
                 operator_repo: OperatorRepo,
                 user_repo: UserRepo,
                 institution_repo: InstitutionRepo
                 ):
        super().__init__()
        self.user_repo = user_repo
        self.operator_repo = operator_repo
        self.institution_repo = institution_repo

    async def create_operator(self, user: CreateOperatorSch, db: AsyncSession) -> int:
        user_exist = await self.user_repo.exist_by_email(user.email, db)
        if user_exist:
            raise errors.HTTPError(code=400, msg="Operator already exists with email, try another")
        await self._get_institution_or_404(user.institution_id, db)
        hashed_password = get_password_hash(user.password)

        new_user = User(
            name=user.name,
            email=user.email,
            phone_number=user.phone_number,
            role=UserRole.OPERATOR,
            address=user.address,
            password=hashed_password,
            institution_id=user.institution_id
        )
        user = await self.user_repo.save(new_user, db)
        return user.id

    async def get_operator_by_id(self, operator_id: int, db: AsyncSession) -> GetOperatorSch:
        operator = await self.operator_repo.get(operator_id, db)
        if not operator or operator.role != UserRole.OPERATOR:
            raise errors.HTTPError(code=404, msg=f"Operator with id {operator_id} not found!")

        await operator.awaitable_attrs.institution
        return GetOperatorSch.from_entity(operator)

    async def get_all_operators(self, search: str | None, sort_by: OperatorSortBy, sort_order: SortOrder,
                                page: int, size: int, db: AsyncSession) -> PaginationResponse[GetOperatorSch]:
        operators, total_elements = await self.operator_repo.get_all_operators(
            search, sort_by, sort_order, page, size, db)

        operator_list = [GetOperatorSch.from_entity(operator) for operator in operators]

        return PaginationResponse[GetOperatorSch](body=operator_list).set_page_info(
            total_elements=total_elements, page=page, size=size)

    async def update_operator(self, sch: UpdateOperatorSch, db: AsyncSession) -> str:
        operator = await self.operator_repo.get(sch.id, db)
        if not operator or operator.role != UserRole.OPERATOR:
            raise errors.HTTPError(code=404, msg=f"Operator with id {sch.id} not found!")

        conflict = await self.user_repo.get_conflicting_user(sch.email, sch.phone_number, db, exclude_id=sch.id)
        if conflict:
            field = "email" if conflict.email == sch.email else "phone number"
            raise errors.HTTPError(code=400, msg=f"User already exists with this {field}, try another")

        if sch.institution_id != operator.institution_id:
            await self._get_institution_or_404(sch.institution_id, db)

        operator.name = sch.name
        operator.email = sch.email
        operator.phone_number = sch.phone_number
        operator.address = sch.address
        operator.institution_id = sch.institution_id
        await self.operator_repo.save(operator, db)
        return "Operator updated successfully"

    async def delete_operator(self, operator_id: int, db: AsyncSession) -> str:
        operator = await self.operator_repo.get(operator_id, db)
        if not operator or operator.role != UserRole.OPERATOR:
            raise errors.HTTPError(code=404, msg=f"Operator with id {operator_id} not found!")

        await self.operator_repo.delete_by_id(operator_id, db)
        return "Operator deleted successfully"


    async def _get_institution_or_404(self, institution_id: int, db: AsyncSession) -> None:
        if not await self.institution_repo.get(institution_id, db):
            raise errors.HTTPError(code=404, msg=f"Institution with id {institution_id} not found!")
