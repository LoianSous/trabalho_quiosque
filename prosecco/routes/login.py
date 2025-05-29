from flask import request, Blueprint, jsonify, url_for, session, redirect
from flask_login import login_required
from prosecco.config import db, limiter, User_type
from werkzeug.security import check_password_hash
from prosecco.models import User
from flask_login import login_user, logout_user

login_auth = Blueprint('login_auth', __name__)

@login_auth.route('/login/auth', methods=['POST'])
@limiter.limit("5 per hour")
def auth():
    email_do_formulario = request.form.get('id') 
    passphrase_do_formulario = request.form.get('passphrase')

    if not email_do_formulario or not passphrase_do_formulario:
        return jsonify(success=False, error="Email e senha são obrigatórios"), 400

    user = db.session.query(User).filter(User.email == email_do_formulario).first()

    if not user:
        return jsonify(success=False, error="Usuário não encontrado"), 404

    if not user.is_active_account():
        return jsonify(success=False, error="Problemas com o cadastro, contacte um administrador"), 403

    if not check_password_hash(user.passphrase, passphrase_do_formulario):
        return jsonify(success=False, error="Credenciais inválidas"), 401

    client_ip = request.remote_addr
    if user.u_type != User_type.ADMIN:
        allowed = any(device.ip_address == client_ip and device.status == 'active' for device in user.devices) # type: ignore
        if not allowed:
            return jsonify(success=False, error="IP não autorizado. Contate um administrador para cadastrar sua máquina."), 403

    login_user(user)
    session.permanent = True

    return jsonify(success=True, redirect_url=url_for('adm')), 200

@login_auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))