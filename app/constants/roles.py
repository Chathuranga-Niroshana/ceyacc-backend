# app/constants/roles.py

ROLE_STUDENT = 1
ROLE_TEACHER = 2
ROLE_ADMIN = 3

ROLE_NAME_MAP = {
    ROLE_STUDENT: "student",
    ROLE_TEACHER: "teacher",
    ROLE_ADMIN: "admin",
}

DEFAULT_ROLES_FOR_DB = [
    {"id": 1, "name": "student"},
    {"id": 2, "name": "teacher"},
    {"id": 3, "name": "admin"},
]
