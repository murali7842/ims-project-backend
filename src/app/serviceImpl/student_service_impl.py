from sqlalchemy.ext.asyncio import AsyncSession
from src.app.common.exception import errors
from src.app.models.enum import PaymentStatus
from src.app.models.student import Student
from src.app.repositories.course_repo import CourseRepo
from src.app.repositories.student_repo import StudentRepo
from src.app.repositories.user_repo import UserRepo
from src.app.schemas.student_sch import CreateStudentSch
from src.app.services.student_service import StudentService


class StudentServiceImpl(StudentService):

    def __init__(self,
                 student_repo: StudentRepo,
                 user_repo: UserRepo,
                 course_repo : CourseRepo
                 ):
        super().__init__()
        self.student_repo = student_repo
        self.user_repo =  user_repo
        self.course_repo = course_repo


    async def create_student(self, sch: CreateStudentSch, db: AsyncSession) -> int:
        student_exist = await self.student_repo.exist_by_email(sch.email, db)
        if student_exist:
            raise errors.HTTPError(code=400, msg="Student already exists with email, try another")

        course = await self.course_repo.get(sch.course_id, db)
        if not course:
            raise errors.HTTPError(code=404, msg="Course not found")

        new_student = Student(
            name=sch.name,
            email=sch.email,
            phone_number=sch.phone_number,
            address=sch.address,
            guardian_name=sch.guardian_name,
            guardian_phone=sch.guardian_phone,
            status=sch.status,
            fee_amount=course.course_fee,
            payment_status = PaymentStatus.UNPAID,
            course_id=sch.course_id,
            institution_id=sch.institution_id,
            batch_id=sch.batch_id
        )
        student = await self.student_repo.save(new_student, db)
        return student.id