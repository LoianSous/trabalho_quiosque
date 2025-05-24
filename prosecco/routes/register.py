from flask import render_template, request, Blueprint, jsonify, redirect, url_for
from prosecco.config import db
from passlib.hash import argon2
from prosecco.models import User

register_new = Blueprint('register_new', __name__)

@register_new.route('/login/new', methods=['POST'])
def new_user():
    username = request.form.get('name')
    email = request.form.get('email')
    passphrase = request.form.get('passphrase')
    
    existing_user = db.session.query(User).filter_by(email=email).first()
    
    if existing_user is not None:
        return jsonify(success=False, error="user aready exists"), 409
    
    hash_passphrase = argon2.hash(passphrase)
    
    new_user = User(name=username, email=email, passphrase=hash_passphrase)
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('login')), 201
