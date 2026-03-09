from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.config.db_config import Base, AsyncSessionLocal


class BaseRepo[T: Base]:

    def __init__(self, model: T):
        super().__init__()
        self.model = model

    async def get(self, id: int, db: AsyncSession | None = None) -> T | None:
        query = select(self.model).where(self.model.id == id)
        if db is None:
            async with AsyncSessionLocal() as session:
                return await self._get(query, session)
        else:
            return await self._get(query, db)

    async def _get(self, query, db):
        result = await db.execute(query)
        return result.scalars().first()

    async def get_all(self, db: AsyncSession | None = None) -> T | None:
        query = select(self.model)
        if db is None:
            async with AsyncSessionLocal() as session:
                return await self._get_all(query, session)
        else:
            return await self._get_all(query, db)

    async def _get_all(self, query, db):
        result = await db.execute(query)
        return result.scalars().all()

    async def save(self, db_obj: T, db: AsyncSession) -> T:
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def save_all(self, db_obj: list[T], db: AsyncSession):
        db.add_all(db_obj)
        await db.commit()

    async def update(self, id: int, obj_data: dict, db: AsyncSession) -> T | None:
        query = update(self.model).where(self.model.id == id).values(**obj_data)
        await db.execute(query)
        await db.commit()
        return await self.get(id, db)

    async def delete_by_id(self, id: int, db: AsyncSession) -> bool:
        query = delete(self.model).where(self.model.id == id)
        await db.execute(query)
        await db.commit()
        return True

    async def delete(self, entity: T, db: AsyncSession):
        await db.delete(entity)
        await db.commit()
