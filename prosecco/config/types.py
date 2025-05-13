from enum import Enum

class User_type(Enum):
    ADMIN = "admin"
    USER = "user"
    
    
class User_state(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"