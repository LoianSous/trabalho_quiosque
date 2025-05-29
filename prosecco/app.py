from flask import Flask, render_template
from flask_login import LoginManager, login_required
from prosecco.config import db, migrate, limiter, User_type, scheduler
from prosecco.utils import access_required, ip_authorized_required
from prosecco.routes import login_auth, register_new, adm_route, upload_route
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv('.env')

prosecco = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'img', 'uploads')

prosecco.secret_key = os.getenv('SECRET_KEY')
prosecco.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)
prosecco.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
prosecco.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
prosecco.config['SCHEDULER_API_ENABLED'] = True
prosecco.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(prosecco)
migrate.init_app(prosecco, db)
limiter.init_app(prosecco)

login_manager = LoginManager()
login_manager.login_view = 'login'  # type: ignore
login_manager.init_app(prosecco)

@login_manager.user_loader
def load_user(user_id):
    from prosecco.models import User
    return db.session.get(User, int(user_id))

with prosecco.app_context():
    from prosecco.models import User, Device, File_trk

prosecco.register_blueprint(login_auth)
prosecco.register_blueprint(register_new)
prosecco.register_blueprint(adm_route)
prosecco.register_blueprint(upload_route)

def ratelimit_exceeded(e):
    return 429

@prosecco.route('/')
@ip_authorized_required
def painel():
    return render_template('painel_exibicao.html')

@prosecco.route('/new')
def reg():
    return render_template('register.html')

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

@prosecco.route('/upload-form')
@login_required
def upload_form():
    return render_template('upload.html')

if __name__ == '__main__':
    scheduler.init_app(prosecco)
    scheduler.start()
    prosecco.run(debug=True)
