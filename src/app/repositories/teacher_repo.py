

from src.app.models.user import User
from src.app.repositories.base import BaseRepo


class TeacherRepo(BaseRepo[User]):

    def __init__(self):
        super().__init__(User)