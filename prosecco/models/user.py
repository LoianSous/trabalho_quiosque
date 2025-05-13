from prosecco.config.database import db
from prosecco.config.types import User_type, User_state

class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    passphrase = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    u_type = db.Column(db.Enum(User_type), nullable=False, default=User_type.USER)
    u_state = db.Collumn(db.Enum(User_state), nullable=False, default=User_state.ACTIVE)
    dt_created = db.Column(db.Integer, default=db.func.strftime('%s', 'now')) 
    dt_updated = db.Column(db.Integer, default=db.func.strftime('%s', 'now'), onupdate=db.func.strftime('%s', 'now'))
    
