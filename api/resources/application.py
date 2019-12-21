from flask_restful import Resource, request
import flask_jwt_extended as jwt
import json
from ..extensions import db
from ..db_meta.user_data import User, UserMainInfo
from ..util.auth import create_acc_token, create_ref_token


class UserLogin(Resource):
    def post(self):
        data = json.loads(request.data)
        username = data.get('username')
        password = data.get('password')
        user = User.find_by_username(username)

        if not user:
            return { 'message': 'User %s is not exist' % username }

        if not password or not User.verify_hash(password, user.password):
            return { 'message': 'User and password don\'t match' }
        else:
            user = User.find_by_username(username)
            user_data = {
                'username': user.username,
                'user_id': user.user_id
            }
            return {
                'message': 'Logged as %s' % user_data.get('username'),
                'username': user_data.get('username'),
                'access_token': create_acc_token(user_data),
                'refresh_token': create_ref_token(user_data)
            }


class UserRegistration(Resource):
    def post(self):
        data = json.loads(request.data)
        username = data['username']
        password = data['password']
        repeat_password = data['repeat_password']

        if password != repeat_password:
            return { 'message': 'Passwords don\'t match' }

        if User.find_by_username(username):
            return { 'message': 'User %s is already exist' % username }

        user = User(
            username=username,
            password=User.generate_hash(password)
        )
        try:
            db.session.add(user)
            db.session.flush()
            user_main_info = UserMainInfo(
                user_id=user.user_id
            )
            db.session.add(user_main_info)
            db.session.commit()
            user_data = {
                'username': user.username,
                'user_id': user.user_id
            }
            return {
                'message': 'Create user %s' % user_data.get('username'),
                'username': user_data.get('username'),
                'access_token': create_acc_token(user_data),
                'refresh_token': create_ref_token(user_data)
            }
        except Exception:
            return {'message': 'Something went wrong'}, 500


class GetUserData(Resource):
    @jwt.jwt_required
    def get(self):
        username = jwt.get_jwt_identity().get('username')
        return {
            'user_data':
                {
                    'username': username
                }
            }


class TokenRefresh(Resource):
    @jwt.jwt_refresh_token_required
    def post(self):
        username = jwt.get_jwt_identity()
        return {
            'access_token': create_acc_token(username)
        }
