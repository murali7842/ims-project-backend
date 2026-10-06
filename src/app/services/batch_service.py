from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.enum import SortOrder
from src.app.schemas.batch_sch import CreateBatchSch, GetBatchSch, UpdateBatchSch, BatchSortBy
from src.app.shared.response import PaginationResponse


class BatchService(ABC):

    @abstractmethod
    async def create_batch(self, sch: CreateBatchSch, db: AsyncSession) -> int:
        pass

    @abstractmethod
    async def get_batch_by_id(self, batch_id: int, db: AsyncSession) -> GetBatchSch:
        pass

    @abstractmethod
    async def get_all_batches(self, search: str | None, sort_by: BatchSortBy, sort_order: SortOrder,
                              page: int, size: int, db: AsyncSession) -> PaginationResponse[GetBatchSch]:
        pass

    @abstractmethod
    async def update_batch(self, batch_id: int, sch: UpdateBatchSch, db: AsyncSession) -> str:
        pass

    @abstractmethod
    async def delete_batch(self, batch_id: int, db: AsyncSession) -> str:
        pass
