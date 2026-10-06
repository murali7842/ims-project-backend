import enum
from pydantic import BaseModel

from src.app.models.course import Course


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
