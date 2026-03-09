from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.batch import Batch
from src.app.repositories.base import BaseRepo


class BatchRepo(BaseRepo[Batch]):

    def __init__(self):
        super().__init__(Batch)

    async def exist_by_name(self, name: str, session: AsyncSession) -> bool:
        query = select(func.count(Batch.id)).where(Batch.name == name)
        result = await session.execute(query)
        return result.scalar() > 0
