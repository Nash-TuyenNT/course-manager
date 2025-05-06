from app.enums.actions import Actions
from app.enums.resourses import Resources
from app.roles.utils import allow_all, is_enrolled_course, is_enrolled_lesson, is_enrolled_attendance, \
    is_enrolled_quiz

STUDENT_PERMISSIONS = {
    Resources.COURSE: {
        Actions.READ: allow_all,
        Actions.ENROLL: allow_all,
        Actions.VIEW_STATUS: is_enrolled_course,
        Actions.COMPLETE: is_enrolled_course
    },
    Resources.LESSON: {
        Actions.READ: allow_all,
        Actions.VIEW_STATUS: is_enrolled_lesson
    },
    Resources.ATTENDANCE: {
        Actions.READ: is_enrolled_attendance,
        Actions.UPDATE: is_enrolled_attendance
    },
    Resources.QUIZ: {
        Actions.READ: allow_all,
        Actions.SUBMIT: is_enrolled_quiz,
    }
}
