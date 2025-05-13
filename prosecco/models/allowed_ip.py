from prosecco.config.database import db
from prosecco.config.types import Device_state

class Allow_ip(db.Model):
    
    __tablename__ = 'Allowed_ips'
    
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    locale = db.Column(db.String(128), nullable=False)
    a_state = db.Column(db.Enum(Device_state), nullable=False, default=Device_state.ACTIVE)
    dt_created = db.Column(db.Integer, default=db.func.strftime('%s', 'now')) 
    dt_updated = db.Column(db.Integer, default=db.func.strftime('%s', 'now'), onupdate=db.func.strftime('%s', 'now'))

    relationship = db.relationship('User', back_populates='allowed_ips')