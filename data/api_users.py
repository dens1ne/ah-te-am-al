import flask
from flask import jsonify, request, make_response

from . import db_session
from .users import User
from .api_jobs import blueprint


@blueprint.route('/api/users')
def get_all_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()

    return jsonify(
        {
            'users':
                [item.to_dict(only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>')
def get_user_by_id(user_id: int):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)

    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)

    return jsonify(
        user.to_dict(only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from'))
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json
                 for key in ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from', 'password']):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()
    user = User()
    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.email = request.json['email']
    user.city_from = request.json['city_from']
    user.hashed_password = request.json['password']
    db_sess.add(user)
    db_sess.commit()

    return make_response({'id': user.id}, 200)


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id: int):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)

    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)
    elif not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from']
                 for key in request.json):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    for key in request.json:
        if key == 'surname':
            user.surname = request.json[key]
        elif key == 'name':
            user.name = request.json[key]
        elif key == 'age':
            user.age = request.json[key]
        elif key == 'position':
            user.position = request.json[key]
        elif key == 'speciality':
            user.speciality = request.json[key]
        elif key == 'address':
            user.address = request.json[key]
        elif key == 'email':
            user.email = request.json[key]
        elif key == 'city_from':
            user.city_from = request.json[key]

    db_sess.add(user)
    db_sess.commit()

    return make_response(jsonify({'success': 'OK'}), 200)


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)

    if not user:
        return make_response(jsonify({'error': 'User not found'}, 404))

    db_sess.delete(user)
    db_sess.commit()

    return make_response(jsonify({'success': 'Deleted'}), 200)
