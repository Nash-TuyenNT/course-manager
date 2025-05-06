from enum import Enum


class Actions(str, Enum):
    COMPLETE = "complete"
    VIEW_STATUS = "view_status"
    SUBMIT = "submit"
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    MANAGE = "manage"
    ENROLL = "enroll"
