from app.enums.actions import Actions
from app.enums.resourses import Resources
from app.roles.utils import allow_all

ADMIN_PERMISSIONS = {
    Resources.COURSE: {
        Actions.CREATE: allow_all,
        Actions.READ: allow_all,
        Actions.UPDATE: allow_all,
        Actions.DELETE: allow_all,
        Actions.MANAGE: allow_all,
    },
    Resources.LESSON: {
        Actions.CREATE: allow_all,
        Actions.READ: allow_all,
        Actions.UPDATE: allow_all,
        Actions.DELETE: allow_all,
    },
    Resources.ATTENDANCE: {
        Actions.CREATE: allow_all,
        Actions.READ: allow_all,
        Actions.UPDATE: allow_all,
        Actions.DELETE: allow_all,
        Actions.MANAGE: allow_all,
    },
    Resources.QUIZ: {
        Actions.CREATE: allow_all,
        Actions.READ: allow_all,
        Actions.UPDATE: allow_all,
        Actions.DELETE: allow_all,
    }
}
