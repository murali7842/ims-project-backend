from sqlalchemy.ext.asyncio import AsyncSession
from src.app.common.exception import errors
from src.app.models.batch import Batch
from src.app.models.enum import SortOrder
from src.app.repositories.batch_repo import BatchRepo
from src.app.schemas.batch_sch import CreateBatchSch, GetBatchSch, UpdateBatchSch, BatchSortBy
from src.app.services.batch_service import BatchService
from src.app.shared.response import PaginationResponse


class BatchServiceImpl(BatchService):

    def __init__(self,
                 batch_repo: BatchRepo,
                 ):
        super().__init__()
        self.batch_repo = batch_repo

    async def create_batch(self, sch: CreateBatchSch, db: AsyncSession) -> int:
        batch_exist = await self.batch_repo.exist_by_name(sch.name, db)
        if batch_exist:
            raise errors.HTTPError(code=400, msg="Batch already exists with name, try another")
        new_batch = Batch(
            name=sch.name,
            timing=sch.timing,
            student_limit=sch.student_limit,
            start_date=sch.start_date,
            end_date=sch.end_date,
            mode=sch.mode,
            course_id=sch.course_id,
            institution_id=sch.institution_id
        )
        batch = await self.batch_repo.save(new_batch, db)
        return batch.id

    async def get_batch_by_id(self, batch_id: int, db: AsyncSession) -> GetBatchSch:
        batch = await self.batch_repo.get(batch_id, db)
        if not batch:
            raise errors.HTTPError(code=404, msg=f"Batch with id {batch_id} not found!")

        return GetBatchSch.from_entity(batch)

    async def get_all_batches(self, search: str | None, sort_by: BatchSortBy, sort_order: SortOrder,
                              page: int, size: int, db: AsyncSession) -> PaginationResponse[GetBatchSch]:
        batches, total_elements = await self.batch_repo.get_all_batches(search, sort_by, sort_order, page, size, db)

        batch_list = [GetBatchSch.from_entity(batch) for batch in batches]

        return PaginationResponse[GetBatchSch](body=batch_list).set_page_info(
            total_elements=total_elements, page=page, size=size)

    async def update_batch(self, batch_id: int, sch: UpdateBatchSch, db: AsyncSession) -> str:
        data = sch.model_dump(exclude_unset=True, exclude_none=True)
        if not data:
            raise errors.HTTPError(code=400, msg="No fields provided to update")

        batch = await self.batch_repo.get(batch_id, db)
        if not batch:
            raise errors.HTTPError(code=404, msg=f"Batch with id {batch_id} not found!")

        if "name" in data and await self.batch_repo.exist_by_name(data["name"], db, exclude_id=batch_id):
            raise errors.HTTPError(code=400, msg="Batch already exists with name, try another")

        await self.batch_repo.update_by_id(batch_id, data, db)
        return "Batch updated successfully"

    async def delete_batch(self, batch_id: int, db: AsyncSession) -> str:
        batch = await self.batch_repo.get(batch_id, db)
        if not batch:
            raise errors.HTTPError(code=404, msg=f"Batch with id {batch_id} not found!")

        await self.batch_repo.delete_by_id(batch_id, db)
        return "Batch deleted successfully"