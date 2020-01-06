import flask_jwt_extended as jwt
from datetime import timedelta

CONST_ACC_TOKEN_EXPIRES = timedelta(minutes=1)
CONST_REF_TOKEN_EXPIRES = timedelta(minutes=30)


def create_acc_token(username):
    return jwt.create_access_token(
        identity=username,
        expires_delta=CONST_ACC_TOKEN_EXPIRES
    )


def create_ref_token(username):
    return jwt.create_refresh_token(
        identity=username,
        expires_delta=CONST_REF_TOKEN_EXPIRES
    )
