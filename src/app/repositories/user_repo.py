from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.config.security import pwd_context
from src.app.models.user import User, OTPRecord
from src.app.repositories.base import BaseRepo


class UserRepo(BaseRepo[User]):

    def __init__(self):
        super().__init__(User)

    async def exist_by_email(self, email: EmailStr, session: AsyncSession) -> bool:
        query = select(func.count(User.id)).where(User.email == email)
        result = await session.execute(query)
        return result.scalar() > 0

    async def get_by_email(self, email: str, db: AsyncSession) -> User:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    async def update_password(self, email: EmailStr, new_password: str, db: AsyncSession) -> None:
        await db.execute(
            update(User)
            .where(User.email == email)
            .values(password=new_password)
        )
        await db.commit()