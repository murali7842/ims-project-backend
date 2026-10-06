from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import select, func, delete, update, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.config.security import pwd_context
from src.app.models.enum import UserRole, SortOrder
from src.app.models.user import User, OTPRecord
from src.app.repositories.base import BaseRepo
from src.app.schemas.user_sch import UserSortBy


class UserRepo(BaseRepo[User]):

    def __init__(self):
        super().__init__(User)

    async def exist_by_email(self, email: EmailStr, session: AsyncSession) -> bool:
        query = select(func.count(User.id)).where(User.email == email)
        result = await session.execute(query)
        return result.scalar() > 0

    async def get_conflicting_user(self, email: str, phone_number: str, db: AsyncSession,
                                   exclude_id: int | None = None) -> User | None:
        """Any other user already holding this email or phone number (both are unique columns)"""
        query = select(User).where(or_(User.email == email, User.phone_number == phone_number))
        if exclude_id is not None:
            query = query.where(User.id != exclude_id)
        return await db.scalar(query.limit(1))

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

    async def get_all_users(self, search: str | None, role: UserRole | None,
                            sort_by: UserSortBy, sort_order: SortOrder,
                            page: int, size: int, db: AsyncSession) -> tuple[list[User], int]:
        query = select(User)

        if role is not None:
            query = query.where(User.role == role)

        if search:
            search_term = f"%{search.strip()}%"
            query = query.where(
                or_(
                    User.name.ilike(search_term),
                    User.email.ilike(search_term),
                    User.phone_number.ilike(search_term)
                )
            )

        total_elements = await db.scalar(select(func.count()).select_from(query.subquery()))
        if not total_elements:
            return [], 0

        sort_column = getattr(User, sort_by.value)
        order = sort_column.asc() if sort_order == SortOrder.ASC else sort_column.desc()

        # User.id as tie-breaker keeps page boundaries stable when sort values repeat
        query = (
            query
            .options(selectinload(User.institution))
            .order_by(order, User.id.desc())
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await db.execute(query)
        return list(result.scalars().all()), total_elements
