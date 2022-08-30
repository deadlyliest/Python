import jwt
import uuid
import datetime

from model import db
from model import User
from functools import wraps
from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from api import create_app as app

bp_user = Blueprint('user', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify(message="É necessário que exista um token para essa requisição."), 401

        try:
          
            data = jwt.decode(token, 'muitosecreto', algorithms=['HS256'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify(message="Token inválido."), 401

        return f(current_user, *args, **kwargs)
    return decorated

@bp_user.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    if not current_user.admin:
        return jsonify(message="Não é possível executar essa função.")

    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify(
        message="Retornando todos os usuários",
        data=output
    )


@bp_user.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    if not current_user.admin:
        return jsonify(message="Não é possível executar essa função.")

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify(message="Nenhum usuário foi encontrado no database.")

    user_data =  {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify(
        message="Retornando usuário...",
        user=user_data
    )


@bp_user.route('/user', methods=['POST'])
@token_required
def create_user(current_user):

    if not current_user.admin:
        return jsonify(message="Não é possível executar essa função.")

    data = request.get_json()

    hashed_passwd = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_passwd, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="Usuário criado com sucesso!")


@bp_user.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user,public_id):

    if not current_user.admin:
        return jsonify(message="Não é possível executar essa função.")

    user = User.query.filter_by(public_id=public_id).first()
    
    if not user:
        return jsonify(message="Nenhum usuário foi encontrado no database.")

    user.admin = True
    db.session.commit()
    
    return jsonify(message="Usuário promovido.") 


@bp_user.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):

    if not current_user.admin:
        return jsonify(message="Não é possível executar essa função.")
    
    user = User.query.filter_by(public_id=public_id).first()
    
    if not user:
        return jsonify(message="Nenhum usuário foi encontrado no database.")

    db.session.delete(user)
    db.session.commit()

    return jsonify(message="Usuário deletado com sucesso.")


# AUTHENTICATION

@bp_user.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Não foi possível verificar', 401, {'WWW-Authenticate': 'Basic realm="Logue!"'})
    
    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Não foi possível verificar', 401, {'WWW-Authenticate': 'Basic realm="Logue!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id}, 'muitosecreto', algorithm="HS256")
       
        return jsonify({'token' : token})
    
    return make_response('Não foi possível verificar', 401, {'WWW-Authenticate': 'Basic realm="Logue!"'})
