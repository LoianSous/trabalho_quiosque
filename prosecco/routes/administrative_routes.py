import json
from flask import Blueprint, request, jsonify
from prosecco.config import db
from werkzeug.security import check_password_hash, generate_password_hash as hash_pass
from prosecco.config.types import User_type
from prosecco.models import File_trk, User, Device
from prosecco.config import User_state, Device_state

adm_route = Blueprint('/adm', __name__)

@adm_route.route('/adm/users', methods=['GET'])
def get_all_users():
    all_users = db.session.query(User).filter(User.u_state != User_state.DELETED.value).all()
    users_list = [user.to_dict() for user in all_users]
    return jsonify(users_list)

@adm_route.route('/adm/user/new', methods=['POST'])
def create_new_user():
    username = request.form.get('name')
    email = request.form.get('email')
    passphrase = request.form.get('password')
    u_type = request.form.get('u_type')
    
    if db.session.query(User).filter(User.email == email).first():
        return jsonify(Sucess=False, error='user already exists'), 409

    if not passphrase:
        return jsonify(success=False, error='Password is required'), 400

    new_user = User(name=username, email=email, passphrase=hash_pass(passphrase), u_type=u_type)
    
    return jsonify(sucess=True), 201
    
    
@adm_route.route('/adm/devices', methods=['GET'])
def get_all_devices():
    all_devices = db.session.query(Device).filter(Device.a_state != Device_state.BLOCKED).all()
    device_list = [device.to_dict() for device in all_devices]
    return jsonify(device_list)    