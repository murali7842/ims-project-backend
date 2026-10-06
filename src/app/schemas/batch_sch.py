import enum
from datetime import date
from pydantic import BaseModel

from src.app.models.batch import Batch
from src.app.models.enum import BatchMode


class BatchSortBy(str, enum.Enum):
    ID = "id"
    NAME = "name"
    START_DATE = "start_date"
    END_DATE = "end_date"
    STUDENT_LIMIT = "student_limit"


class CreateBatchSch(BaseModel):
    name: str
    timing: str
    student_limit: int
    start_date: date
    end_date: date
    mode: BatchMode
    course_id: int
    institution_id: int

class UpdateBatchSch(BaseModel):
    name: str | None = None
    timing: str | None = None
    student_limit: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    mode: BatchMode | None = None
    course_id: int | None = None

class GetBatchSch(BaseModel):
    id: int
    name: str
    timing: str
    student_limit: int
    start_date: date
    end_date: date
    mode: BatchMode
    course_id: int
    institution_id: int

    @staticmethod
    def from_entity(batch: Batch):
        return GetBatchSch(
            id= batch.id,
            name= batch.name,
            timing= batch.timing,
            student_limit= batch.student_limit,
            start_date= batch.start_date,
            end_date= batch.end_date,
            mode= batch.mode,
            course_id= batch.course_id,
            institution_id= batch.institution_id
        )


