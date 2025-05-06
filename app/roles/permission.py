from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException

from app.enums.actions import Actions
from app.enums.resourses import Resources
from app.enums.roles import Roles
from app.models.user import User
from app.roles.admin import ADMIN_PERMISSIONS
from app.roles.student import STUDENT_PERMISSIONS
from app.roles.teacher import TEACHER_PERMISSIONS

# --- Roles Permissions (all callables) ---
ROLE_PERMISSIONS = {
    Roles.admin: ADMIN_PERMISSIONS,
    Roles.teacher: TEACHER_PERMISSIONS,
    Roles.student: STUDENT_PERMISSIONS
}


class RoleObject:
    def __init__(self, name: Roles):
        self.name = name
        self.permissions = ROLE_PERMISSIONS.get(name, {})

    def can(self, user: User, action: Actions, resource: Resources, target: Optional[dict] = None) -> bool:
        resource_rules = self.permissions.get(resource, {})
        rule_fn = resource_rules.get(action)

        if not callable(rule_fn):
            return False

        return rule_fn(user, target)


def check_permission(user: User, action: Actions, resource: Resources, target: Optional[dict] = None):
    role = RoleObject(user.role)

    if not role.can(user, action, resource, target):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=f"You do not have permission to {action.name} this {resource.name}"
        )
