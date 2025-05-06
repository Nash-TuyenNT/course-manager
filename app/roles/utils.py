from typing import Optional

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.quiz_models import LessonQuiz
from app.models.student_attendance import AttendanceSession
from app.models.user import User


# --- Permission Logic Functions ---
def allow_all(user: User, target: Optional[dict] = None) -> bool:
    return True


def deny_all(user: User, target: Optional[dict] = None) -> bool:
    return False


def is_owner(user: User, target: Optional[dict]) -> bool:
    return target and target.creator_id == user.id


def is_enrolled_course(user: User, target: Optional[Course]) -> bool:
    return target and any(u.user_id == user.id for u in target.users)


def is_enrolled_attendance(user: User, target: Optional[AttendanceSession]) -> bool:
    return target and is_enrolled_course(user, target.course)


def is_enrolled_lesson(user: User, target: Optional[Lesson]) -> bool:
    return target and is_enrolled_course(user, target.course)


def is_enrolled_quiz(user: User, target: Optional[LessonQuiz]) -> bool:
    return target and is_enrolled_lesson(user, target.lesson)
