from enum import Enum


class Roles(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"
