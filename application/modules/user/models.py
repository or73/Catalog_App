"""
File Path: application/modules/user/models.py
Description: User models for App - Define User models
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime

from flask_login import UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import check_password_hash, generate_password_hash
from application.setup import db
from application.crud import CRUDMixin

from config import Config
# Methods
from category.methods import CategoryMethod
from item.methods import ItemMethod


class User(UserMixin, CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # User authentication fields
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(150), unique=True)
    # User fields
    active = db.Column(db.Boolean)  # To know if auth is active in system or not
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(150))
    # User control
    authenticated = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime(), default=datetime.datetime.now())
    provider = db.Column(db.String(10), default='local')   # 0: local - 1: facebook - 2: google
    profile = db.Column(db.String(10), default='user')     # 0: user - 1:Administrator
    session_token = db.Column(db.String(150), unique=True)

    # ---------------------------------------------------------------------
    def __init__(self, authenticated, email, first_name, last_name,
                 password, picture, profile, provider, username, session_token):
        # User authentication fields
        self.email = email
        self.password_hash(password)
        self.username = username
        # User fields
        self.active = True
        self.first_name = first_name
        self.last_name = last_name
        self.picture = picture

        # User control
        self.authenticated = authenticated
        self.set_last_login()
        self.profile = profile
        self.provider = provider
        if session_token:
            self.session_token = session_token
        else:
            self.session_token = self.generate_auth_token(600)

    # ----------------------------- METHODS ------------------------------
    def validate_password(self, password):
        """validate provided password with password in DB"""
        return check_password_hash(self.password, password)

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        print('user-models -  is_authenticated')
        return True

    def is_owner_category(self, category_name):
        return self.id == CategoryMethod.get_owner_by_name(category_name)

    def is_owner_item(self, item_name):
        return self.id == ItemMethod.get_owner_by_name(item_name)

    def generate_auth_token(self, expiration=600):
        s = Serializer(Config.SECRET_KEY,
                       expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(Config.SECRET_KEY)

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None   # Valid token, but expired
        except BadSignature:
            return None    # Invalid token
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # ----------------------------- GETTERS ---------------------------------
    def get_id(self):
        return self.session_token

    def get_email(self):
        """email getter"""
        return self.email

    def get_username(self):
        """username getter"""
        return self.username

    def get_first_name(self):
        """first_name getter"""
        return self.first_name

    def get_last_name(self):
        """last_name getter"""
        return self.last_name

    def get_last_login(self):
        return self.last_login

    def get_session_token(self):
        return self.session_token

    # ----------------------------- SETTERS ---------------------------------
    def set_email(self, email):
        """email setter"""
        self.email = email

    def password_hash(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def set_username(self, username):
        """username setter"""
        self.username = username

    def set_first_name(self, first_name):
        """first_name setter"""
        self.first_name = first_name

    def set_last_name(self, last_name):
        """last_name setter"""
        self.last_name = last_name

    def set_last_login(self):
        self.last_login = datetime.datetime.now()

    def set_session_token(self):
        self.session_token = self.generate_auth_token(600)
