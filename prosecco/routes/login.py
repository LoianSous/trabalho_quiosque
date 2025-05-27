from flask import render_template, request, Blueprint, jsonify, redirect, url_for
from prosecco.config import db
from werkzeug.security import check_password_hash
from prosecco.config import limiter
from prosecco.models import User

login_auth = Blueprint('login_auth', __name__)

@login_auth.route('/login/auth', methods=['POST'])
@limiter.limit("5 per hour")
def auth():
    email_do_formulario = request.form.get('id') 
    passphrase_do_formulario = request.form.get('passphrase')

    if not email_do_formulario or not passphrase_do_formulario:
        return jsonify(success=False, error="Email e senha são obrigatórios"), 400

    user = db.session.query(User).filter(User.email == email_do_formulario).first()

    
    if user and check_password_hash(user.passphrase, passphrase_do_formulario):

        return jsonify(success=True, redirect_url=url_for('adm')), 200
    else:
        return jsonify(success=False, error="Credenciais inválidas"), 401