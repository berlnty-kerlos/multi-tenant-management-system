from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class TaskStatusEnum(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"