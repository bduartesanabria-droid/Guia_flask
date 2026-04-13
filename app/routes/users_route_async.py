from flask import Blueprint, request, jsonify
from app.models.users import User
from app import db

bp = Blueprint('userAsync', __name__, url_prefix='/UserAsync')

# 📌 LISTAR
@bp.route('/index', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


# 📌 CREAR
@bp.route('/add', methods=['POST'])
def create_user():
    data = request.json

    new_user = User(
        nameUser=data['nameUser'],
        email=data['email']   # 🔥 IMPORTANTE
    )

    new_user.set_password(data['passwordUser'])  # 🔐 HASH
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


# 📌 ACTUALIZAR
@bp.route('/update/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    if user:
        data = request.json

        user.nameUser = data['nameUser']
        user.email = data['email']

        if data.get('passwordUser'):
            user.set_password(data['passwordUser'])  # 🔐 HASH

        db.session.commit()

        return jsonify({'message': 'User updated successfully'})

    return jsonify({'message': 'User not found'}), 404


# 📌 ELIMINAR
@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})

    return jsonify({'message': 'User not found'}), 404