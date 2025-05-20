from prosecco.config.database import db
from prosecco.config.types import Device_state

class Device(db.Model):
    
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    locale = db.Column(db.String(128), nullable=False)
    a_state = db.Column(db.Enum(Device_state, name='device_state'), nullable=False, default=Device_state.ACTIVE)
    dt_created = db.Column(db.Integer, default=db.func.strftime('%s', 'now')) 
    dt_updated = db.Column(db.Integer, default=db.func.strftime('%s', 'now'), onupdate=db.func.strftime('%s', 'now'))

    user = db.relationship('User', back_populates='devices')
