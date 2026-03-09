from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.exception import errors
from src.app.config.security import get_password_hash
from src.app.models.enum import UserRole
from src.app.models.user import User
from src.app.repositories.user_repo import UserRepo
from src.app.schemas.user_sch import UserRegSch
from src.app.services.user_service import UserService


class UserServiceImpl(UserService):

    def __init__(self,
                 user_repo: UserRepo,
                 ):
        super().__init__()
        self.user_repo = user_repo

    async def reg_user(self, user: UserRegSch, db: AsyncSession) -> int:
        user_exist = await self.user_repo.exist_by_email(user.email, db)
        if user_exist:
            raise errors.HTTPError(code=400, msg="User already exists with email, try another")
        hashed_password = get_password_hash(user.password)

        new_user = User(
            name=user.name,
            email=user.email,
            phone_number=user.phone_number,
            role=UserRole.ADMIN,
            address=user.address,
            password=hashed_password
        )
        user = await self.user_repo.save(new_user, db)
        return user.id
