from src.app.models.student_assessment import StudentAssessmentQuestion
from src.app.repositories.base import BaseRepo


class StudentAssessmentQuestionRepo(BaseRepo[StudentAssessmentQuestion]):

    def __init__(self):
        super().__init__(StudentAssessmentQuestion)
