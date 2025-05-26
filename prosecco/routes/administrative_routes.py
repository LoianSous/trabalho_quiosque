from flask import Blueprint, request, jsonify
from prosecco.config import db
from werkzeug.security import check_password_hash
from prosecco.models import File_trk, User
from prosecco.config import User_state

adm_route = Blueprint('/adm', __name__)

@adm_route.route('/adm/users')
def get_all_users():
    all_users = db.session.query(User).filter(User.u_state != User_state.DELETED.value).all()
    users_list = [user.to_dict() for user in all_users]
    return jsonify(users_list)

@adm_route.route('/adm/user/new')
def create_new_user():
    username = request.form.get('name')
    email = request.form.get('email')
    u_type = request.form.get('u_type')
    
    if db.session.query(User).filter(User.email == email).first():
        return jsonify(Sucess= False, 'user aready exist')
    
    