from sqlalchemy.ext.asyncio import AsyncSession
from src.app.common.exception import errors
from src.app.models.course import Course
from src.app.repositories.course_repo import CourseRepo
from src.app.repositories.user_repo import UserRepo
from src.app.schemas.course_sch import CreateCourseSch, GetCourseSch
from src.app.services.course_service import CourseService


class CourseServiceImpl(CourseService):

    def __init__(self,
                 course_repo: CourseRepo,
                 user_repo: UserRepo
                 ):
        super().__init__()
        self.user_repo = user_repo
        self.course_repo = course_repo

    async def create_course(self, sch: CreateCourseSch, db: AsyncSession) -> int:
        course_exist = await self.course_repo.exist_by_name(sch.name, db)
        if course_exist:
            raise errors.HTTPError(code=400, msg="Course already exists with name, try another")

        new_course = Course(
            name=sch.name,
            description=sch.description,
            duration=sch.duration,
            course_fee = sch.course_fee,
            institution_id=sch.institution_id,
            teacher_id=sch.teacher_id
        )
        course = await self.course_repo.save(new_course, db)
        return course.id

    async def get_course_by_id(self, course_id: int, db: AsyncSession) -> GetCourseSch:
        course = await self.course_repo.get(course_id, db)
        if not course:
            raise errors.HTTPError(code=404, msg=f"Course with id {course_id} not found!")

        return GetCourseSch.from_entity(course)
