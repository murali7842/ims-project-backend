from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.student_assessment import StudentAssessmentQuestion, StudentAssessmentQuestionOption, \
    StudentAssessmentAttempt
from src.app.repositories.base import BaseRepo


class StudentAssessmentAttemptRepo(BaseRepo[StudentAssessmentAttempt]):

    def __init__(self):
        super().__init__(StudentAssessmentAttempt)

    async def check_attempted_assessment(self, student_id: int, assessment_id: int, db: AsyncSession) -> bool:
        stmt = select(StudentAssessmentAttempt).where(
            StudentAssessmentAttempt.student_id == student_id,
            StudentAssessmentAttempt.student_assessment_id == assessment_id
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None