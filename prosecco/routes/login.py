from flask import render_template, request, Blueprint, jsonify, redirect, url_for
from prosecco.config import db
from werkzeug.security import check_password_hash
from prosecco.config import limiter
from prosecco.models import User

login_auth = Blueprint('login_auth', __name__)

@login_auth.route('/login/auth', methods=['POST'])
@limiter.limit("5 per hour")
def auth():
    user_id = request.form.get('id')
    passphrase = request.form.get('passphrase')

    user = db.session.query(User).filter_by(email=user_id).first()

    if user and check_password_hash(user.passphrase, passphrase):
        return jsonify(success=True, redirect_url=url_for('adm'))
    else:
        return jsonify(success=False, error="invalid credentials"), 401
