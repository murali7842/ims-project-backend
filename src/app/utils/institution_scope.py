from src.app.common.exception import errors
from src.app.models.enum import UserRole
from src.app.models.user import User


def resolve_institution_id(user: User, institution_id: int | None) -> int | None:
    """Admin can view all institutions or filter by one; operator is always scoped to own institution"""
    if user.role == UserRole.ADMIN:
        return institution_id

    if user.role == UserRole.TEACHER:
        # teacher data is scoped by the courses they teach (resolve_teacher_id), institution filter is optional
        return institution_id

    if user.institution_id is None:
        raise errors.HTTPError(code=403, msg="Operator is not linked to any institution")
    return user.institution_id


def resolve_teacher_id(user: User) -> int | None:
    """Teacher only sees data of the courses they teach; None for admin/operator means no teacher filter"""
    return user.id if user.role == UserRole.TEACHER else None


def ensure_teacher_owns(user: User, teacher_id: int | None, label: str) -> None:
    """Teacher can open a record only when it belongs to one of their own courses"""
    if user.role == UserRole.TEACHER and teacher_id != user.id:
        raise errors.HTTPError(code=403, msg=f"You can only access {label} of your own courses")
