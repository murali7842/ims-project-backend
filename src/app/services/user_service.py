from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas.user_sch import UserRegSch


class UserService(ABC):

    @abstractmethod
    async def reg_user(self, sch: UserRegSch, db: AsyncSession) -> int:
        pass