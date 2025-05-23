from flask import Flask, render_template, Blueprint, redirect
from dotenv import load_dotenv
from prosecco.config import db, migrate, limiter
from prosecco.routes import login_auth
import os

load_dotenv('.env')

prosecco = Flask(__name__)


prosecco.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
prosecco.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(prosecco)
migrate.init_app(prosecco, db)
limiter.init_app(prosecco)

with prosecco.app_context():
    from prosecco.models import User, Device, File_trk


prosecco.register_blueprint(login_auth)
@prosecco.errorhandler(429)
def ratelimit_exceeded(e):
    return redirect('https://http.cat/429'), 429

@prosecco.route('/')
def painel():
    return render_template('painel_exibicao.html')

@prosecco.route('/login')
def login():
    return render_template('painel_login.html')

@prosecco.route('/adm')
def adm():
    return render_template('painel_adm.html')



if __name__ == '__main__':
    prosecco.run(debug=True)