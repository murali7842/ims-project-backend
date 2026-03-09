from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.schemas.batch_sch import CreateBatchSch,GetBatchSch


class BatchService(ABC):

    @abstractmethod
    async def create_batch(self, sch: CreateBatchSch, db: AsyncSession) -> int:
        pass

    @abstractmethod
    async def get_batch_by_id(self, batch_id: int, db: AsyncSession) -> GetBatchSch:
        pass