from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv('.env')

prosecco = Flask(__name__)

prosecco.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

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