from flask import Blueprint, request, jsonify
from prosecco.config import db
from werkzeug.security import generate_password_hash as hash_pass
from prosecco.models import User, Device, device
from prosecco.config import User_state 


adm_route = Blueprint('/adm', __name__)



# -------------------- usuarios -----------------------------------------------------
@adm_route.route('/adm/users', methods=['GET'])
def get_all_users():
    all_users = db.session.query(User).filter(User.u_state != User_state.DELETED).all()
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

    new_user = User(name=username, email=email, passphrase=hash_pass(passphrase), u_type=u_type, u_state=User_state.ACTIVE) #type:ignore
        
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(sucess=True), 201

@adm_route.route('/adm/user/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = db.session.query(User).filter(User.id == user_id, User.u_state != User_state.DELETED).first()
    if not user:
        return jsonify(success=False, error='User not found'), 404

    data = request.json
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.passphrase = hash_pass(data['password'])
    if 'u_type' in data:
        user.u_type = data['u_type']

    db.session.commit()
    return jsonify(success=True, message='User updated successfully'), 200


@adm_route.route('/adm/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.session.query(User).filter(User.id == user_id, User.u_state != User_state.DELETED).first()
    if not user:
        return jsonify(success=False, error='User not found'), 404

    user.u_state = User_state.DELETED
    db.session.commit()
    return jsonify(success=True, message='User soft-deleted successfully'), 200



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
    
    
@adm_route.route('/adm/device/<int:device_id>', methods=['PATCH'])
def update_device(device_id):
    device = db.session.query(Device).filter(Device.id == device_id).first()
    if not device:
        return jsonify(success=False, error='Device not found'), 404

    data = request.json
    if 'ip' in data:
        device.ip = data['ip']
    if 'locale' in data:
        device.locale = data['locale']
    if 'group' in data:
        device.group = data['group']
    if 'user_id' in data:
        device.user_id = data['user_id']

    db.session.commit()
    return jsonify(success=True, message='Device updated successfully'), 200


@adm_route.route('/adm/device/<int:device_id>', methods=['DELETE'])
def soft_delete_device(device_id):
    device = db.session.query(Device).filter(Device.id == device_id).first()
    if not device:
        return jsonify(success=False, error='Device not found'), 404

    device.a_state = 'DELETED'
    db.session.commit()
    return jsonify(success=True, message='Device deleted successfully'), 200
