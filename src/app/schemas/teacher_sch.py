from pydantic import EmailStr, BaseModel
from src.app.models.user import User
from src.app.schemas.base import DropDownSch
from src.app.schemas.institution_sch import InstitutionDropDown


class CreateTeacherSch(BaseModel):
    name: str
    email: EmailStr
    password:str
    phone_number:str
    address:str
    institution_id: int

class UpdateTeacherSch(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: str
    address: str
    institution_id: int

class GetTeacherDetailsSch(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str
    address: str
    role: str
    institution: InstitutionDropDown | None = None

    @staticmethod
    def from_entity(teacher: User) -> 'GetTeacherDetailsSch':

        return GetTeacherDetailsSch(
            id=teacher.id,
            name=teacher.name,
            email=teacher.email,
            phone_number=teacher.phone_number,
            address=teacher.address,
            role=teacher.role,
            institution=(
                InstitutionDropDown.from_entity(teacher.institution)
                if teacher.institution else None
            )
        )


class TeacherCourseSch(BaseModel):
    id: int
    name: str
    total_batches: int
    batches: list[DropDownSch]

class TeacherDetailSch(GetTeacherDetailsSch):
    total_courses: int
    total_batches: int
    courses: list[TeacherCourseSch]

    @staticmethod
    def build(teacher: User, course_batch_rows) -> "TeacherDetailSch":
        """Group flat (course, batch) rows into courses with their batches - single O(n) pass"""
        courses: dict[int, TeacherCourseSch] = {}
        for row in course_batch_rows:
            course = courses.get(row.course_id)
            if course is None:
                course = courses[row.course_id] = TeacherCourseSch(
                    id=row.course_id, name=row.course_name, total_batches=0, batches=[])
            if row.batch_id is not None:  # course without any batch yet
                course.batches.append(DropDownSch(id=row.batch_id, name=row.batch_name))
                course.total_batches += 1

        return TeacherDetailSch(
            **GetTeacherDetailsSch.from_entity(teacher).model_dump(),
            total_courses=len(courses),
            total_batches=sum(course.total_batches for course in courses.values()),
            courses=list(courses.values())
        )
