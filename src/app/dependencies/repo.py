from src.app.repositories.assessment_institution_publish_repo import AssessmentInstitutionPublishRepo
from src.app.repositories.batch_repo import BatchRepo
from src.app.repositories.course_repo import CourseRepo
from src.app.repositories.institution_repo import InstitutionRepo
from src.app.repositories.operator_repo import OperatorRepo
from src.app.repositories.otp_record_repo import OTPRecordRepo
from src.app.repositories.payment_repo import PaymentRepo
from src.app.repositories.student_assessment_attempt_repo import StudentAssessmentAttemptRepo
from src.app.repositories.student_assessment_question_option_repo import StudentAssessmentQuestionOptionRepo
from src.app.repositories.student_assessment_question_repo import StudentAssessmentQuestionRepo
from src.app.repositories.student_assessment_repo import StudentAssessmentRepo
from src.app.repositories.student_repo import StudentRepo
from src.app.repositories.teacher_repo import TeacherRepo
from src.app.repositories.user_repo import UserRepo


def get_institution_repo() -> InstitutionRepo:
    return InstitutionRepo()

def get_user_repo() -> UserRepo:
    return UserRepo()

def get_otp_repo() -> OTPRecordRepo:
    return  OTPRecordRepo()

def get_operator_repo() -> OperatorRepo:
    return OperatorRepo()

def get_teacher_repo() -> TeacherRepo:
    return TeacherRepo()

def get_course_repo() -> CourseRepo:
    return CourseRepo()

def get_batch_repo() -> BatchRepo:
    return BatchRepo()

def get_student_repo() -> StudentRepo:
    return StudentRepo()

def get_payment_repo() -> PaymentRepo:
    return PaymentRepo()

def get_student_assessment_repo() -> StudentAssessmentRepo:
    return StudentAssessmentRepo()


def get_student_assessment_question_repo() -> StudentAssessmentQuestionRepo:
    return StudentAssessmentQuestionRepo()

def get_student_assessment_question_option_repo() -> StudentAssessmentQuestionOptionRepo:
    return StudentAssessmentQuestionOptionRepo()

def get_assessment_institution_publish_repo() -> AssessmentInstitutionPublishRepo:
    return AssessmentInstitutionPublishRepo()

def get_assessment_attempt_repo() -> StudentAssessmentAttemptRepo:
    return StudentAssessmentAttemptRepo()
