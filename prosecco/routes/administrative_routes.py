import json
from flask import Blueprint, request, jsonify
from prosecco.config import db
from werkzeug.security import generate_password_hash as hash_pass
from prosecco.models import User, Device, device
from prosecco.config import User_state 


adm_route = Blueprint('/adm', __name__)



# -------------------- usuarios -----------------------------------------------------
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

    new_user = User(name=username, email=email, passphrase=hash_pass(passphrase), u_type=u_type, u_state=User_state.ACTIVE)
        
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(sucess=True), 201


# ----------- telas--------------------------------------------
@adm_route.route('/adm/devices', methods=['GET'])
def get_all_devices():
    all_devices = db.session.query(Device).all()
    device_list = [device.to_dict() for device in all_devices]
    return jsonify(device_list)    


@adm_route.route('/adm/device/new', methods=['POST'])
def add_new_device():
    ip = request.form.get('ip')
    locale = request.form.get('ip')
    group = request.form.get('group')
    user_id = request.form.get('user')
    
    
    if db.session.query(Device).filter(Device.ip == ip) != None:
        return jsonify(sucess=False, error='this device aready on system'), 409
    
    new_display = Device(user_id=user_id, ip=ip, group=group, locale=locale)
    
    db.session.add(new_display)
    db.session.commit()
    
    return jsonify(sucess=True, message='device added succesfull'), 201
    