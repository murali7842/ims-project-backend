from pydantic import EmailStr
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.student import Student
from src.app.models.user import User
from src.app.repositories.base import BaseRepo


class StudentRepo(BaseRepo[Student]):

    def __init__(self):
        super().__init__(Student)

    async def exist_by_email(self, email: EmailStr, session: AsyncSession) -> bool:
        query = select(func.count(User.id)).where(User.email == email)
        result = await session.execute(query)
        return result.scalar() > 0
