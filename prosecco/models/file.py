from prosecco.config.database import db
from prosecco.config.types import File_state

class File(db.Model):
    
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(128), nullable=False)
    file = db.Column(db.LargeBinary, nullable=False)
    File_state = db.Column(db.Enum(File_state), nullable=False, default=File_state.UPLOADED)
    dt_created = db.Column(db.Integer, default=db.func.strftime('%s', 'now')) 
    dt_updated = db.Column(db.Integer, default=db.func.strftime('%s', 'now'), onupdate=db.func.strftime('%s', 'now'))
    
    relationship = db.relationship('User', back_populates='files')
    

