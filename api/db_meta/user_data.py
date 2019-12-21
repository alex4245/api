from passlib.hash import pbkdf2_sha256 as sha256
from ..extensions import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True, nullable=False, index=True)
    password = db.Column(db.Unicode, nullable=False)
    user_main_info = db.relationship("UserMainInfo", uselist=False, back_populates="user") 

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class UserMainInfo(db.Model):
    __tablename__ = 'user_main_info'

    user_main_info = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False, unique=True)
    full_name = db.Column(db.Unicode)
    status = db.Column(db.Unicode)
    user = db.relationship("User", back_populates="user_main_info")
