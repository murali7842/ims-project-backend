from sqlalchemy.ext.asyncio import AsyncSession
from src.app.common.exception import errors
from src.app.models.course import Course
from src.app.models.enum import PaymentStatus, SortOrder
from src.app.models.student import Student
from src.app.repositories.batch_repo import BatchRepo
from src.app.repositories.course_repo import CourseRepo
from src.app.repositories.student_repo import StudentRepo
from src.app.repositories.user_repo import UserRepo
from src.app.schemas.student_sch import CreateStudentSch, GetStudentSch, UpdateStudentSch, StudentSortBy
from src.app.services.student_service import StudentService
from src.app.models.user import User
from src.app.shared.response import PaginationResponse
from src.app.utils.institution_scope import resolve_institution_id


class StudentServiceImpl(StudentService):

    def __init__(self,
                 student_repo: StudentRepo,
                 user_repo: UserRepo,
                 course_repo : CourseRepo,
                 batch_repo: BatchRepo
                 ):
        super().__init__()
        self.student_repo = student_repo
        self.user_repo =  user_repo
        self.course_repo = course_repo
        self.batch_repo = batch_repo


    async def create_student(self, sch: CreateStudentSch, db: AsyncSession) -> int:
        await self._check_unique(sch.email, sch.phone_number, db)
        course = await self._get_valid_course(sch, db)

        new_student = Student(
            name=sch.name,
            email=sch.email,
            phone_number=sch.phone_number,
            address=sch.address,
            guardian_name=sch.guardian_name,
            guardian_phone=sch.guardian_phone,
            status=sch.status,
            fee_amount=course.course_fee,
            paid_amount=0.0,
            balance_amount=course.course_fee,
            payment_status = PaymentStatus.UNPAID,
            course_id=sch.course_id,
            institution_id=sch.institution_id,
            batch_id=sch.batch_id
        )
        student = await self.student_repo.save(new_student, db)
        return student.id

    async def get_student_by_id(self, student_id: int, db: AsyncSession) -> GetStudentSch:
        student = await self.student_repo.get(student_id, db)
        if not student:
            raise errors.HTTPError(code=404, msg=f"Student with id {student_id} not found!")

        return GetStudentSch.from_entity(student)

    async def get_all_students(self, user: User, search: str | None, institution_id: int | None,
                               course_id: int | None, batch_id: int | None,
                               sort_by: StudentSortBy, sort_order: SortOrder,
                               page: int, size: int, db: AsyncSession) -> PaginationResponse[GetStudentSch]:
        # operator always gets own institution students, admin gets all or the selected institution
        institution_id = resolve_institution_id(user, institution_id)
        students, total_elements = await self.student_repo.get_all_students(
            search, institution_id, course_id, batch_id, sort_by, sort_order, page, size, db)

        student_list = [GetStudentSch.from_entity(student) for student in students]

        return PaginationResponse[GetStudentSch](body=student_list).set_page_info(
            total_elements=total_elements, page=page, size=size)

    async def update_student(self, sch: UpdateStudentSch, db: AsyncSession) -> str:
        student = await self.student_repo.get(sch.id, db)
        if not student:
            raise errors.HTTPError(code=404, msg=f"Student with id {sch.id} not found!")

        await self._check_unique(sch.email, sch.phone_number, db, exclude_id=sch.id)

        if (sch.course_id, sch.batch_id, sch.institution_id) != \
                (student.course_id, student.batch_id, student.institution_id):
            course = await self._get_valid_course(sch, db)
            if course.id != student.course_id:
                # new course means a new fee; already paid amount carries over
                student.fee_amount = course.course_fee
                student.refresh_payment_status()

        student.name = sch.name
        student.email = sch.email
        student.phone_number = sch.phone_number
        student.address = sch.address
        student.guardian_name = sch.guardian_name
        student.guardian_phone = sch.guardian_phone
        student.status = sch.status
        student.institution_id = sch.institution_id
        student.course_id = sch.course_id
        student.batch_id = sch.batch_id
        await self.student_repo.save(student, db)
        return "Student updated successfully"

    async def delete_student(self, student_id: int, db: AsyncSession) -> str:
        student = await self.student_repo.get(student_id, db)
        if not student:
            raise errors.HTTPError(code=404, msg=f"Student with id {student_id} not found!")

        await self.student_repo.delete_by_id(student_id, db)
        return "Student deleted successfully"

    async def _check_unique(self, email: str, phone_number: str, db: AsyncSession,
                            exclude_id: int | None = None) -> None:
        conflict = await self.student_repo.get_conflicting_student(email, phone_number, db, exclude_id)
        if conflict:
            field = "email" if conflict.email == email else "phone number"
            raise errors.HTTPError(code=400, msg=f"Student already exists with this {field}, try another")

    async def _get_valid_course(self, sch: CreateStudentSch, db: AsyncSession) -> Course:
        """Course and batch must exist, and the batch must belong to that course and institution"""
        course = await self.course_repo.get(sch.course_id, db)
        if not course:
            raise errors.HTTPError(code=404, msg=f"Course with id {sch.course_id} not found!")

        batch = await self.batch_repo.get(sch.batch_id, db)
        if not batch:
            raise errors.HTTPError(code=404, msg=f"Batch with id {sch.batch_id} not found!")

        if batch.course_id != sch.course_id or batch.institution_id != sch.institution_id:
            raise errors.HTTPError(code=400, msg="Batch does not belong to the given course and institution")
        return course
