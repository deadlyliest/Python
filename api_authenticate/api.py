import json
import uuid
import jwt

from flask import Flask
from model import configure as config_db

def create_app():
    app = Flask(__name__)

    app.config['JSON_SORT_KEYS'] = False
    app.config['SECRET_KEY'] = 'muitosecreto'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/danie/Documents/Python/Flask/api_authenticate/db.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    config_db(app)


    from user import bp_user
    app.register_blueprint(bp_user)


    app.run(debug=True)
    return app

# DATABASE

# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     public_id = db.Column(db.String(50), unique=True)
#     name = db.Column(db.String(50))
#     password = db.Column(db.String(80))
#     admin = db.Column(db.Boolean)

# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(50))
#     complete = db.Column(db.Boolean)
#     user_id = db.Column(db.Integer)


# ROUTES



# # TODO ROUTES

# @app.route('/todo', methods=['GET'])
# @token_required
# def get_all_todos(current_user):
#     data = request.get_json()

#     new_todo = Todo(text=data['text'], complete=False, user_id=current_user.id)
#     db.session.add(new_todo)
#     db.session.commit()

#     return jsonify(message="Todo criado!")


# @app.route('/todo/<todo_id>', methods=['GET'])
# @token_required
# def get_one_todo(current_user, todo_id):
#     ...


# @app.route('/todo', methods=['POST'])
# @token_required
# def create_todo(current_user):
#     ...


# @app.route('/todo/<todo_id>', methods=['PUT'])
# @token_required
# def complete_todo(current_user, todo_id):
#     ...


# @app.route('/todo/<todo_id>', methods=['DELETE'])
# @token_required
# def delete_todo(current_user, todo_id):
#     ...



if __name__ == '__main__':
    create_app()