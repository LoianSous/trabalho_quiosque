from prosecco.config import db
from prosecco.config import User_type, User_state
import time

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    passphrase = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    u_type = db.Column(db.Enum(User_type, name="user_type"), nullable=False, default=User_type.USER)
    u_state = db.Column(db.Enum(User_state, name="user_state"), nullable=False, default=User_state.ACTIVE)

    dt_created = db.Column(db.Integer, default=lambda: int(time.time()))
    dt_updated = db.Column(db.Integer, default=lambda: int(time.time()), onupdate=lambda: int(time.time()))

    devices = db.relationship('Device', back_populates='user')
    files = db.relationship('File_trk', back_populates='user')