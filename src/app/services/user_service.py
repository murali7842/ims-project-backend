from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.enum import UserRole, SortOrder
from src.app.schemas.user_sch import UserRegSch, GetUserSch, UpdateUserSch, UserSortBy
from src.app.shared.response import PaginationResponse


class UserService(ABC):

    @abstractmethod
    async def reg_user(self, sch: UserRegSch, db: AsyncSession) -> int:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int, db: AsyncSession) -> GetUserSch:
        pass

    @abstractmethod
    async def get_all_users(self, search: str | None, role: UserRole | None,
                            sort_by: UserSortBy, sort_order: SortOrder,
                            page: int, size: int, db: AsyncSession) -> PaginationResponse[GetUserSch]:
        pass

    @abstractmethod
    async def update_user(self, sch: UpdateUserSch, db: AsyncSession) -> str:
        pass

    @abstractmethod
    async def delete_user(self, user_id: int, current_user_id: int, db: AsyncSession) -> str:
        pass
