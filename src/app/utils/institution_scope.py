from src.app.common.exception import errors
from src.app.models.enum import UserRole
from src.app.models.user import User


def resolve_institution_id(user: User, institution_id: int | None) -> int | None:
    """Admin can view all institutions or filter by one; operator is always scoped to own institution"""
    if user.role == UserRole.ADMIN:
        return institution_id

    if user.institution_id is None:
        raise errors.HTTPError(code=403, msg="Operator is not linked to any institution")
    return user.institution_id
