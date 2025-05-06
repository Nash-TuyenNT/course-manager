from enum import Enum


class Resources(str, Enum):
    ATTENDANCE = "attendance"
    COURSE = "course"
    LESSON = "lesson"
    QUIZ = "quiz"
