import enum
from datetime import date
from pydantic import BaseModel

from src.app.models.batch import Batch
from src.app.models.course import Course
from src.app.models.enum import BatchMode
from src.app.schemas.base import DropDownSch


class CourseSortBy(str, enum.Enum):
    ID = "id"
    NAME = "name"
    DURATION = "duration"
    COURSE_FEE = "course_fee"

class CreateCourseSch(BaseModel):
    name: str
    description: str
    duration: str
    course_fee: float
    institution_id: int
    teacher_id: int

class UpdateCourseSch(BaseModel):
    name: str | None = None
    description: str | None = None
    duration: str | None = None
    course_fee: float | None = None
    teacher_id: int | None = None

class GetCourseSch(BaseModel):
    id: int
    name: str
    description: str | None
    duration: str | None
    course_fee: float
    institution_id: int | None
    teacher_id: int


    @staticmethod
    def from_entity(course: Course):
        return GetCourseSch(
            id=course.id,
            name=course.name,
            description=course.description,
            duration=course.duration,
            course_fee=course.course_fee,
            institution_id=course.institution_id,
            teacher_id=course.teacher_id
        )


class CourseBatchSch(BaseModel):
    id: int
    name: str
    timing: str
    mode: BatchMode
    start_date: date
    end_date: date
    student_limit: int
    total_students: int

    @staticmethod
    def from_entity(batch: Batch, total_students: int) -> "CourseBatchSch":
        return CourseBatchSch(
            id=batch.id,
            name=batch.name,
            timing=batch.timing,
            mode=batch.mode,
            start_date=batch.start_date,
            end_date=batch.end_date,
            student_limit=batch.student_limit,
            total_students=total_students
        )

class CourseDetailSch(BaseModel):
    id: int
    name: str
    description: str | None
    duration: str | None
    course_fee: float
    institution: DropDownSch | None
    teacher: DropDownSch | None
    total_batches: int
    total_students: int
    batches: list[CourseBatchSch]

    @staticmethod
    def from_entity(course: Course, institution_name: str | None, teacher_name: str | None,
                    batch_rows) -> "CourseDetailSch":
        batches = [CourseBatchSch.from_entity(row.Batch, row.total_students) for row in batch_rows]
        return CourseDetailSch(
            id=course.id,
            name=course.name,
            description=course.description,
            duration=course.duration,
            course_fee=course.course_fee,
            institution=DropDownSch.of(course.institution_id, institution_name),
            teacher=DropDownSch.of(course.teacher_id, teacher_name),
            total_batches=len(batches),
            total_students=sum(batch.total_students for batch in batches),
            batches=batches
        )
