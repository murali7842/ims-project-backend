import enum


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"

class BatchMode(enum.Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    HYBRID = "HYBRID"

class StudentStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class PaymentStatus(enum.Enum):
    PAID = "PAID",
    UNPAID = "UNPAID",
    PARTIALLY_PAID = "PARTIALLY_PAID"

class QuestionType(str, enum.Enum):
    SHORT_ANSWER = "SHORT_ANSWER"
    PARAGRAPH = "PARAGRAPH"
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    CHECKBOXES = "CHECKBOXES"
    DROPDOWN = "DROPDOWN"
    FILE_UPLOAD = "FILE_UPLOAD"
    RATING = "RATING"
    LINEAR_SCALE = "LINEAR_SCALE"

class ResponseStatus(str, enum.Enum):
    NO_RESPONSE = "NO_RESPONSE"
    CORRECT = "CORRECT"
    IN_CORRECT = "IN_CORRECT"

class PublishStatus(str, enum.Enum):
    PUBLISHED = "PUBLISHED"
    DRAFT = "DRAFT"

class AttemptStatus(str, enum.Enum):
    IN_PROGRESS = "IN_PROGRESS"
    SUBMITTED = "SUBMITTED"
    EVALUATED = "EVALUATED"

class MediaType(str, enum.Enum):
    IMAGE = "IMAGE",
    DOC = "DOC"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    LINK = "LINK"
