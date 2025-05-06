from app.enums.actions import Actions
from app.enums.resourses import Resources
from app.roles.utils import allow_all, is_owner

TEACHER_PERMISSIONS = {
    Resources.COURSE: {
        Actions.CREATE: allow_all,
        Actions.READ: allow_all,
        Actions.UPDATE: is_owner,
        Actions.DELETE: is_owner,
        Actions.MANAGE: is_owner,
    },
    Resources.LESSON: {
        Actions.CREATE: allow_all,
        Actions.READ: allow_all,
        Actions.UPDATE: is_owner,
        Actions.DELETE: is_owner,
    },
    Resources.ATTENDANCE: {
        Actions.CREATE: allow_all,
        Actions.READ: allow_all,
        Actions.UPDATE: is_owner,
        Actions.DELETE: is_owner,
        Actions.MANAGE: allow_all,
    },
    Resources.QUIZ: {
        Actions.CREATE: allow_all,
        Actions.READ: allow_all,
        Actions.UPDATE: allow_all,
        Actions.DELETE: allow_all,
    }
}
