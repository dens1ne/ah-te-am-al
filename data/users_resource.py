from flask_restful import reqparse, abort, Resource
from flask import jsonify

from data.db_session import create_session
from data.users import User


parser = reqparse.RequestParser()
parser.add_argument('surname', type=str, required=True)
parser.add_argument('name', type=str, required=True)
parser.add_argument('age', type=int, required=True)
parser.add_argument('position', type=str, required=True)
parser.add_argument('speciality', type=str, required=True)
parser.add_argument('email', type=str, required=True)
parser.add_argument('password', type=str, required=True)
parser.add_argument('city_from', type=str, required=True)
parser.add_argument('address', type=str, required=True)


def abort_if_user_doesnt_exist(user_id):
    db_sess = create_session()
    user = db_sess.query(User).get(user_id)

    if not user:
        abort(404, messgae=f"User {user_id} doesn't exist")

    return user, db_sess


class UsersResource(Resource):
    def get(self, user_id):
        user, _ = abort_if_user_doesnt_exist(user_id)
        return jsonify({'user': user.to_dict(only=(
            'id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from'))})

    def delete(self, user_id):
        user, db_sess = abort_if_user_doesnt_exist(user_id)
        db_sess.delete(user)
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        db_sess = create_session()
        users = db_sess.query(User).all()
        return jsonify({'users': [user.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from'
                  )) for user in users]})

    def post(self):
        args = parser.parse_args()
        db_sess = create_session()
        user = User()
        user.name = args['name']
        user.surname = args['surname']
        user.age = args['age']
        user.position = args['position']
        user.speciality = args['speciality']
        user.address = args['address']
        user.email = args['email']
        user.city_from = args['city_from']
        user.hashed_password = args['password']
        db_sess.add(user)
        db_sess.commit()

        return jsonify({'user_id': user.id})
