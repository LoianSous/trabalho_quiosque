from prosecco.config.database import db

class Login(db.Model):
    __tablename__ = 'login'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.email'), nullable=False)
    passphrase = db.Column(db.String(255), nullable=False)
    dt_login = db.Column(db.Integer, default=db.func.strftime('%s', 'now'))
    dt_logout = db.Column(db.Integer, default=db.func.strftime('%s', 'now'))
    
    user = db.relationship('User', backref='logins')