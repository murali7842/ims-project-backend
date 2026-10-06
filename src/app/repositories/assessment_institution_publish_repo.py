from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.student_assessment import AssessmentInstitutionPublish
from src.app.repositories.base import BaseRepo


class AssessmentInstitutionPublishRepo(BaseRepo[AssessmentInstitutionPublish]):

    def __init__(self):
        super().__init__(AssessmentInstitutionPublish)

    async def delete_by_assessment_id(self, assessment_id: int, db: AsyncSession) -> None:
        """Does not commit, so it runs in the same transaction as the caller's save/delete"""
        await db.execute(
            delete(AssessmentInstitutionPublish).where(AssessmentInstitutionPublish.assessment_id == assessment_id)
        )
