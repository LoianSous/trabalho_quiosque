from enum import Enum

class User_type(Enum):
    ADMIN = "admin"
    USER = "user"
    
    
class User_state(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    PENDING = 'pending'
    
    
class File_state(Enum):
    UPLOADED = "uploaded"
    PROCESSED = "processed"
    DELETED = "deleted"


class Device_state(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"