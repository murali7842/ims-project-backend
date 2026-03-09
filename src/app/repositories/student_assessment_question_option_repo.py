
from src.app.models.student_assessment import StudentAssessmentQuestion, StudentAssessmentQuestionOption
from src.app.repositories.base import BaseRepo


class StudentAssessmentQuestionOptionRepo(BaseRepo[StudentAssessmentQuestionOption]):

    def __init__(self):
        super().__init__(StudentAssessmentQuestionOption)