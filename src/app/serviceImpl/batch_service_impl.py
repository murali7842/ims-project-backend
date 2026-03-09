from sqlalchemy.ext.asyncio import AsyncSession
from src.app.common.exception import errors
from src.app.models.batch import Batch
from src.app.repositories.batch_repo import BatchRepo
from src.app.schemas.batch_sch import CreateBatchSch, GetBatchSch
from src.app.services.batch_service import BatchService


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