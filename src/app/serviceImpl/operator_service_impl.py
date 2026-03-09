from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.exception import errors
from src.app.config.security import get_password_hash
from src.app.models.enum import UserRole
from src.app.models.user import User
from src.app.repositories.operator_repo import OperatorRepo
from src.app.repositories.user_repo import UserRepo
from src.app.schemas.operator_sch import CreateOperatorSch
from src.app.services.operator_service import OperatorService


class OperatorServiceImpl(OperatorService):

    def __init__(self,
                 operator_repo: OperatorRepo,
                 user_repo: UserRepo
                 ):
        super().__init__()
        self.user_repo = user_repo
        self.operator_repo = operator_repo

    async def create_operator(self, user: CreateOperatorSch, db: AsyncSession) -> int:
        user_exist = await self.user_repo.exist_by_email(user.email, db)
        if user_exist:
            raise errors.HTTPError(code=400, msg="Operator already exists with email, try another")
        hashed_password = get_password_hash(user.password)

        new_user = User(
            name=user.name,
            email=user.email,
            phone_number=user.phone_number,
            role=UserRole.OPERATOR,
            address=user.address,
            password=hashed_password,
            institution_id=user.institution_id
        )
        user = await self.user_repo.save(new_user, db)
        return user.id