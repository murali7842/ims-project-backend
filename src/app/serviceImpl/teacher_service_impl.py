from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.exception import errors
from src.app.config.security import get_password_hash
from src.app.models.enum import UserRole
from src.app.models.user import User
from src.app.repositories.teacher_repo import TeacherRepo
from src.app.repositories.user_repo import UserRepo
from src.app.schemas.teacher_sch import CreateTeacherSch
from src.app.services.teacher_service import TeacherService


class TeacherServiceImpl(TeacherService):

    def __init__(self,
                 teacher_repo: TeacherRepo,
                 user_repo: UserRepo
                 ):
        super().__init__()
        self.user_repo = user_repo
        self.teacher_repo = teacher_repo

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