from flask_restful import Resource, request
from flask import g
import flask_jwt_extended as jwt
import json

from ..extensions import db
from ..db_meta.user_data import User, UserMainInfo
from ..util.auth import create_acc_token, create_ref_token
from .ma_schemas.user_info import MaUserMainInfo
from ..util.marshmallow_tools import ma_validation

import logging


class StartPage(Resource):
    @jwt.jwt_required
    def get(self):
        return {'start': 'start'}


class AccountOptions(Resource):
    @jwt.jwt_required
    def get(self):
        logging.info('fsfafa')
        user_data = jwt.get_jwt_identity()
        umi = UserMainInfo.query.filter_by(
            user_id=user_data.get('user_id')
        ).one()
        return {
            'full_name': umi.full_name,
            'status': umi.status
        }

    @jwt.jwt_required
    @ma_validation(MaUserMainInfo)
    def patch(self):
        user_data = jwt.get_jwt_identity()
        umi = UserMainInfo.query.filter_by(user_id=user_data.get('user_id')).one()
        umi.full_name = g.post_parametrs.get('full_name'),
        umi.status=g.post_parametrs.get('status')
        db.session.commit()
