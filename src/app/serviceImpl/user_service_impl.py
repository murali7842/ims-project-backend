from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.exception import errors
from src.app.config.security import get_password_hash
from src.app.models.enum import UserRole, SortOrder
from src.app.models.user import User
from src.app.repositories.user_repo import UserRepo
from src.app.schemas.user_sch import UserRegSch, GetUserSch, UpdateUserSch, UserSortBy
from src.app.services.user_service import UserService
from src.app.shared.response import PaginationResponse


class UserServiceImpl(UserService):

    def __init__(self,
                 user_repo: UserRepo,
                 ):
        super().__init__()
        self.user_repo = user_repo

    async def reg_user(self, user: UserRegSch, db: AsyncSession) -> int:
        user_exist = await self.user_repo.exist_by_email(user.email, db)
        if user_exist:
            raise errors.HTTPError(code=400, msg="User already exists with email, try another")
        hashed_password = get_password_hash(user.password)

        new_user = User(
            name=user.name,
            email=user.email,
            phone_number=user.phone_number,
            role=UserRole.ADMIN,
            address=user.address,
            password=hashed_password
        )
        user = await self.user_repo.save(new_user, db)
        return user.id

    async def get_user_by_id(self, user_id: int, db: AsyncSession) -> GetUserSch:
        user = await self.user_repo.get(user_id, db)
        if not user:
            raise errors.HTTPError(code=404, msg=f"User with id {user_id} not found!")

        await user.awaitable_attrs.institution
        return GetUserSch.from_entity(user)

    async def get_all_users(self, search: str | None, role: UserRole | None,
                            sort_by: UserSortBy, sort_order: SortOrder,
                            page: int, size: int, db: AsyncSession) -> PaginationResponse[GetUserSch]:
        users, total_elements = await self.user_repo.get_all_users(
            search, role, sort_by, sort_order, page, size, db)

        user_list = [GetUserSch.from_entity(user) for user in users]

        return PaginationResponse[GetUserSch](body=user_list).set_page_info(
            total_elements=total_elements, page=page, size=size)

    async def update_user(self, sch: UpdateUserSch, db: AsyncSession) -> str:
        user = await self.user_repo.get(sch.id, db)
        if not user:
            raise errors.HTTPError(code=404, msg=f"User with id {sch.id} not found!")

        conflict = await self.user_repo.get_conflicting_user(sch.email, sch.phone_number, db, exclude_id=sch.id)
        if conflict:
            field = "email" if conflict.email == sch.email else "phone number"
            raise errors.HTTPError(code=400, msg=f"User already exists with this {field}, try another")

        user.name = sch.name
        user.email = sch.email
        user.phone_number = sch.phone_number
        user.address = sch.address
        await self.user_repo.save(user, db)
        return "User updated successfully"

    async def delete_user(self, user_id: int, current_user_id: int, db: AsyncSession) -> str:
        if user_id == current_user_id:
            raise errors.HTTPError(code=400, msg="You cannot delete your own account")

        user = await self.user_repo.get(user_id, db)
        if not user:
            raise errors.HTTPError(code=404, msg=f"User with id {user_id} not found!")

        await self.user_repo.delete_by_id(user_id, db)
        return "User deleted successfully"
