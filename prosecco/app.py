from flask import Flask, render_template, redirect, abort, request
from flask_login import LoginManager, login_required, current_user
from prosecco.config import db, migrate, limiter, User_type
from prosecco.routes import login_auth, register_new, adm_route
import os
from dotenv import load_dotenv
from datetime import timedelta
from functools import wraps

load_dotenv('.env')

prosecco = Flask(__name__)


prosecco.secret_key = os.getenv('SECRET_KEY')
prosecco.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
prosecco.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
prosecco.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(prosecco)
migrate.init_app(prosecco, db)
limiter.init_app(prosecco)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(prosecco)

def access_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            if current_user.u_type == User_type.ADMIN:
                return f(*args, **kwargs)
            
            if current_user.u_type not in allowed_roles:
                abort(403)
                
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator

def ip_authorized_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)

        if current_user.u_type != User_type.ADMIN:
            client_ip = request.remote_addr
            allowed = any(device.ip_address == client_ip and device.status == 'active' for device in current_user.devices)
            if not allowed:
                abort(403)
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    from prosecco.models import User
    return db.session.get(User, int(user_id))

with prosecco.app_context():
    from prosecco.models import User, Device, File_trk


prosecco.register_blueprint(login_auth)
prosecco.register_blueprint(register_new)
prosecco.register_blueprint(adm_route)

def ratelimit_exceeded(e):
    return redirect('https://http.cat/429'), 429

@prosecco.route('/')
@ip_authorized_required
def painel():
    return render_template('painel_exibicao.html')

@prosecco.route('/login')
def login():
    return render_template('painel_login.html')

@prosecco.route('/login/recovery')
def recovery():
    return render_template('recuperar_senha.html')

@prosecco.route('/adm')
@login_required
@access_required(User_type.ADMIN)
def adm():
    return render_template('painel_adm.html')

@prosecco.route('/new')
def reg():
    return render_template('register.html')



if __name__ == '__main__':
    prosecco.run(debug=True)