from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.institution import Institution
from src.app.repositories.base import BaseRepo


class InstitutionRepo(BaseRepo[Institution]):

    def __init__(self):
        super().__init__(Institution)

    async def is_institution_exists(self, name: str, db: AsyncSession) -> bool:
        result = await db.scalar(
            select(func.count()).where(
                Institution.name.ilike(name)
            )
        )
        return result > 0

    async def get_multiple(self, ids: list[int], db: AsyncSession):
        stmt = select(Institution).where(Institution.id.in_(ids))
        result = await db.execute(stmt)
        return result.scalars().all()