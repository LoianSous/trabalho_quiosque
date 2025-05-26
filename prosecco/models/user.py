from prosecco.config import db
from prosecco.config import User_type, User_state
from datetime import datetime, timezone

class User(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    passphrase = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    u_type = db.Column(db.Enum(User_type, name="user_type"), nullable=False, default=User_type.USER)
    u_state = db.Column(db.Enum(User_state, name="user_state"), nullable=False, default=User_state.PENDING)

    dt_created = db.Column(db.Integer, default=lambda: datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
    dt_updated = db.Column(db.Integer, default=lambda: datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), onupdate=lambda: datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))

    devices = db.relationship('Device', back_populates='user')
    files = db.relationship('File_trk', back_populates='user')
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "u_state": self.u_state.value 
        }