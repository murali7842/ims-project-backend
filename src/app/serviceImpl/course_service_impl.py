from sqlalchemy.ext.asyncio import AsyncSession
from src.app.common.exception import errors
from src.app.models.course import Course
from src.app.models.enum import SortOrder
from src.app.repositories.course_repo import CourseRepo
from src.app.repositories.user_repo import UserRepo
from src.app.schemas.course_sch import CreateCourseSch, GetCourseSch, UpdateCourseSch, CourseSortBy
from src.app.services.course_service import CourseService
from src.app.shared.response import PaginationResponse


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

    async def get_all_courses(self, search: str | None, sort_by: CourseSortBy, sort_order: SortOrder,
                              page: int, size: int, db: AsyncSession) -> PaginationResponse[GetCourseSch]:
        courses, total_elements = await self.course_repo.get_all_courses(search, sort_by, sort_order, page, size, db)

        course_list = [GetCourseSch.from_entity(course) for course in courses]

        return PaginationResponse[GetCourseSch](body=course_list).set_page_info(
            total_elements=total_elements, page=page, size=size)

    async def update_course(self, course_id: int, sch: UpdateCourseSch, db: AsyncSession) -> str:
        data = sch.model_dump(exclude_unset=True, exclude_none=True)
        if not data:
            raise errors.HTTPError(code=400, msg="No fields provided to update")

        course = await self.course_repo.get(course_id, db)
        if not course:
            raise errors.HTTPError(code=404, msg=f"Course with id {course_id} not found!")

        if "name" in data and await self.course_repo.exist_by_name(data["name"], db, exclude_id=course_id):
            raise errors.HTTPError(code=400, msg="Course already exists with name, try another")

        await self.course_repo.update_by_id(course_id, data, db)
        return "Course updated successfully"

    async def delete_course(self, course_id: int, db: AsyncSession) -> str:
        course = await self.course_repo.get(course_id, db)
        if not course:
            raise errors.HTTPError(code=404, msg=f"Course with id {course_id} not found!")

        await self.course_repo.delete_by_id(course_id, db)
        return "Course deleted successfully"
