from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.exception import errors
from src.app.config.security import get_password_hash
from src.app.models.enum import UserRole
from src.app.models.user import User
from src.app.repositories.institution_repo import InstitutionRepo
from src.app.repositories.teacher_repo import TeacherRepo
from src.app.repositories.user_repo import UserRepo
from src.app.schemas.teacher_sch import CreateTeacherSch, GetTeacherDetailsSch, UpdateTeacherSch
from src.app.services.teacher_service import TeacherService
from src.app.shared.response import PaginationResponse


class TeacherServiceImpl(TeacherService):

    def __init__(self,
                 teacher_repo: TeacherRepo,
                 user_repo: UserRepo,
                 institution_repo: InstitutionRepo
                 ):
        super().__init__()
        self.user_repo = user_repo
        self.teacher_repo = teacher_repo
        self.institution_repo = institution_repo

    async def create_teacher(self, user: CreateTeacherSch, db: AsyncSession) -> int:
        user_exist = await self.user_repo.exist_by_email(user.email, db)
        if user_exist:
            raise errors.HTTPError(code=400, msg="Teacher already exists with email, try another")
        hashed_password = get_password_hash(user.password)

        new_user = User(
            name=user.name,
            email=user.email,
            phone_number=user.phone_number,
            role=UserRole.TEACHER,
            address=user.address,
            password=hashed_password,
            institution_id=user.institution_id
        )
        user = await self.user_repo.save(new_user, db)
        return user.id

    async def get_all_teacher(self, search: str | None, page: int, size: int, db: AsyncSession) -> PaginationResponse[GetTeacherDetailsSch]:

        teachers, total_elements = await self.teacher_repo.get_all_teacher(search, page, size, db)

        teacher_list = [GetTeacherDetailsSch.from_entity(teacher) for teacher in teachers]

        return PaginationResponse[GetTeacherDetailsSch](body=teacher_list).set_page_info(
            total_elements=total_elements, page=page, size=size)

    async def get_teacher_by_id(self, teacher_id: int, db: AsyncSession) -> GetTeacherDetailsSch:
        """Get a single teacher by ID"""
        teacher = await self.teacher_repo.get_by_id(teacher_id, db)
        if not teacher:
            raise errors.HTTPError(code=404, msg="Teacher not found")
        return GetTeacherDetailsSch.from_entity(teacher)

    async def update_teacher(self, sch: UpdateTeacherSch, db: AsyncSession) -> str:
        teacher = await self.teacher_repo.get(sch.id, db)
        if not teacher or teacher.role != UserRole.TEACHER:
            raise errors.HTTPError(code=404, msg=f"Teacher with id {sch.id} not found!")

        conflict = await self.user_repo.get_conflicting_user(sch.email, sch.phone_number, db, exclude_id=sch.id)
        if conflict:
            field = "email" if conflict.email == sch.email else "phone number"
            raise errors.HTTPError(code=400, msg=f"User already exists with this {field}, try another")

        if sch.institution_id != teacher.institution_id:
            institution = await self.institution_repo.get(sch.institution_id, db)
            if not institution:
                raise errors.HTTPError(code=404, msg=f"Institution with id {sch.institution_id} not found!")

        teacher.name = sch.name
        teacher.email = sch.email
        teacher.phone_number = sch.phone_number
        teacher.address = sch.address
        teacher.institution_id = sch.institution_id
        await self.teacher_repo.save(teacher, db)
        return "Teacher updated successfully"

    async def delete_teacher(self, teacher_id: int, db: AsyncSession) -> str:
        teacher = await self.teacher_repo.get(teacher_id, db)
        if not teacher or teacher.role != UserRole.TEACHER:
            raise errors.HTTPError(code=404, msg=f"Teacher with id {teacher_id} not found!")

        await self.teacher_repo.delete_by_id(teacher_id, db)
        return "Teacher deleted successfully"
