import enum
from pydantic import BaseModel

from src.app.models.institution import Institution
from src.app.schemas.base import DropDownSch


class InstitutionSortBy(str, enum.Enum):
    ID = "id"
    NAME = "name"
    EMAIL = "email"

class InstitutionCreateSch(BaseModel):
    name: str
    email: str
    address: str
    contact_number: str

    def fill_entity(self, entity: Institution):
        entity.name = self.name
        entity.email = self.email
        entity.address = self.address
        entity.contact_number = self.contact_number

class InstitutionUpdateSch(InstitutionCreateSch):
    id: int

class InstitutionSch(BaseModel):
    id: int
    name: str
    email: str
    address: str
    contact_number: str | None

    @staticmethod
    def from_entity(entity: Institution):
        return InstitutionSch(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            address=entity.address,
            contact_number=entity.contact_number
        )

class InstitutionDropDown(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_entity(entity: Institution) -> "InstitutionDropDown":
        return InstitutionDropDown(
            id=entity.id,
            name=entity.name
        )


class InstitutionCourseSch(BaseModel):
    id: int
    name: str
    course_fee: float
    teacher: DropDownSch | None
    batches: list[DropDownSch]

class InstitutionDetailSch(InstitutionSch):
    total_courses: int
    total_batches: int
    total_teachers: int
    total_operators: int
    total_students: int
    courses: list[InstitutionCourseSch]

    @staticmethod
    def build(details, course_batch_rows) -> "InstitutionDetailSch":
        """Group flat (course, batch) rows into courses with their batches - single O(n) pass"""
        courses: dict[int, InstitutionCourseSch] = {}
        for row in course_batch_rows:
            course = courses.get(row.course_id)
            if course is None:
                course = courses[row.course_id] = InstitutionCourseSch(
                    id=row.course_id,
                    name=row.course_name,
                    course_fee=row.course_fee,
                    teacher=DropDownSch.of(row.teacher_id, row.teacher_name),
                    batches=[]
                )
            if row.batch_id is not None:  # course without any batch yet
                course.batches.append(DropDownSch(id=row.batch_id, name=row.batch_name))

        return InstitutionDetailSch(
            **InstitutionSch.from_entity(details.Institution).model_dump(),
            total_courses=details.total_courses,
            total_batches=details.total_batches,
            total_teachers=details.total_teachers,
            total_operators=details.total_operators,
            total_students=details.total_students,
            courses=list(courses.values())
        )
