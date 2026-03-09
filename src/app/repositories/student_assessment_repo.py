from src.app.models.student_assessment import StudentAssessment
from src.app.repositories.base import BaseRepo


class StudentAssessmentRepo(BaseRepo[StudentAssessment]):

    def __init__(self):
        super().__init__(StudentAssessment)