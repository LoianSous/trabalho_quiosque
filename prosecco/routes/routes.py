# from flask import Blueprint, jsonify, request
# from merlot.models import User
# from merlot.config.database import db

# bp = Blueprint('main', __name__)

# @bp.route('/users', methods=['GET'])
# def list_users():
#     users = User.query.all()
#     return jsonify([{'id': u.id, 'name': u.name, 'email': u.email} for u in users])

# @bp.route('/users', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     user = User(name=data['name'], email=data['email'])
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 201
from prosecco import main
from flask import render_template

@prosecco.route('/')
def painel():
    return render_template('painel_exibicao.html')

@prosecco.route('/login')
def login():
    return render_template('painel_login.html')

@prosecco.route('/adm')
def adm():
    return render_template('painel_adm.html')