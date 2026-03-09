


from src.app.models.student_assessment import AssessmentInstitutionPublish
from src.app.repositories.base import BaseRepo


class AssessmentInstitutionPublishRepo(BaseRepo[AssessmentInstitutionPublish]):

    def __init__(self):
        super().__init__(AssessmentInstitutionPublish)