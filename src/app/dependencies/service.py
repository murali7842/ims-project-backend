from fastapi import Depends

from src.app.dependencies.repo import get_institution_repo, get_user_repo, get_otp_repo, get_operator_repo, \
    get_teacher_repo, get_course_repo, get_batch_repo, get_student_repo, get_payment_repo, get_student_assessment_repo, \
    get_student_assessment_question_repo, get_student_assessment_question_option_repo, \
    get_assessment_institution_publish_repo, get_assessment_attempt_repo
from src.app.models.institution import Institution
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
from src.app.serviceImpl.auth_service_impl import AuthServiceImpl
from src.app.serviceImpl.batch_service_impl import BatchServiceImpl
from src.app.serviceImpl.course_service_impl import CourseServiceImpl
from src.app.serviceImpl.institution_service_impl import InstitutionServiceImpl
from src.app.serviceImpl.operator_service_impl import OperatorServiceImpl
from src.app.serviceImpl.payment_service_impl import PaymentServiceImpl
from src.app.serviceImpl.student_assessment_service_impl import StudentAssessmentServiceImpl
from src.app.serviceImpl.student_service_impl import StudentServiceImpl
from src.app.serviceImpl.teacher_service_impl import TeacherServiceImpl
from src.app.serviceImpl.user_service_impl import UserServiceImpl
from src.app.services.auth_service import AuthService
from src.app.services.batch_service import BatchService
from src.app.services.course_service import CourseService
from src.app.services.institution_service import InstitutionService
from src.app.services.operator_service import OperatorService
from src.app.services.payment_service import PaymentService
from src.app.services.student_assessment_service import StudentAssessmentService
from src.app.services.student_service import StudentService
from src.app.services.teacher_service import TeacherService
from src.app.services.user_service import UserService


def get_institution_service(institution_repo: InstitutionRepo = Depends(get_institution_repo),

                          ) -> InstitutionService:
    return InstitutionServiceImpl(institution_repo)

def get_user_service(user_repo: UserRepo = Depends(get_user_repo),

                          ) -> UserService:
    return UserServiceImpl(user_repo)

def get_auth_service(user_repo: UserRepo = Depends(get_user_repo),
                     otp_repo : OTPRecordRepo = Depends(get_otp_repo)
                     # serializer: URLSafeTimedSerializer = Depends(get_serializer),
                     # email_service: EmailService = Depends(get_email_service),
                     # verification_token_service: VerificationTokenService = Depends(
                     #     get_verification_token_service)
                     ) -> AuthService:
    return AuthServiceImpl(user_repo,otp_repo)

def get_operator_service(operator_repo: OperatorRepo = Depends(get_operator_repo),
        user_repo: UserRepo = Depends(get_user_repo)

                          ) -> OperatorService:
    return OperatorServiceImpl(operator_repo,user_repo)

def get_teacher_service(teacher_repo: TeacherRepo = Depends(get_teacher_repo),
                        user_repo: UserRepo = Depends(get_user_repo)

                          ) -> TeacherService:
    return TeacherServiceImpl(teacher_repo,user_repo)

def get_course_service(course_repo: CourseRepo = Depends(get_course_repo),
                        user_repo: UserRepo = Depends(get_user_repo)

                          ) -> CourseService:
    return CourseServiceImpl(course_repo,user_repo)

def get_batch_service(batch_repo: BatchRepo = Depends(get_batch_repo)
                        # user_repo: UserRepo = Depends(get_user_repo)
                          ) -> BatchService:
    return BatchServiceImpl(batch_repo)
def get_student_service(student_repo: StudentRepo = Depends(get_student_repo),
                        user_repo: UserRepo = Depends(get_user_repo),
                        course_repo : CourseRepo = Depends(get_course_repo)
                          ) -> StudentService:
    return StudentServiceImpl(student_repo,user_repo,course_repo)

def get_payment_service(payment_repo: PaymentRepo = Depends(get_payment_repo),
                        user_repo: UserRepo = Depends(get_user_repo),
                        student_repo: StudentRepo = Depends(get_student_repo),
                          ) -> PaymentService:
    return PaymentServiceImpl(payment_repo,user_repo,student_repo)

def get_student_assessment_service(
        student_assessment_repo: StudentAssessmentRepo = Depends(get_student_assessment_repo),
        student_assessment_question_repo: StudentAssessmentQuestionRepo =
        Depends(get_student_assessment_question_repo),
        student_assessment_question_option_repo: StudentAssessmentQuestionOptionRepo =
        Depends(get_student_assessment_question_option_repo),
        assessment_institution_publish_repo: AssessmentInstitutionPublishRepo = Depends(get_assessment_institution_publish_repo),
        institution_repo: InstitutionRepo = Depends(get_institution_repo),
        # student_repo: StudentRepo = Depends(get_student_repo),
        student_assessment_attempt_repo: StudentAssessmentAttemptRepo = Depends(get_assessment_attempt_repo)

) -> StudentAssessmentService:
    return StudentAssessmentServiceImpl(student_assessment_repo, student_assessment_question_repo,
                                        student_assessment_question_option_repo, assessment_institution_publish_repo,institution_repo,
                                        student_assessment_attempt_repo)
