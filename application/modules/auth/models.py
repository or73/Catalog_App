"""
File path: application/modules/auth/models.py
Description: Auth models for App - Define auth/login data model
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime

from setup import db
from crud import CRUDMixin


class Auth(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Log-In
    login_time = db.Column(db.DateTime, default=datetime.datetime.now())
    # Log-Out
    logout_time = db.Column(db.DateTime, default=None)

    # ---------------------------------------------------------------------
    def __init__(self, user_id):
        # User authentication fields
        self.user_id = user_id
        self.login_time = self.set_time()
        self.logout_time = None

    def __repr__(self):
        return '<Login {}>'.format(self.user_id)

    @staticmethod
    def set_time():
        return datetime.datetime.now()

    def get_user_id(self):
        return self.user_id

    def get_login_time(self):
        return self.login_time

    def get_logout_time(self):
        return self.logout_time

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_logout_time(self):
        self.logout_time = self.set_time()

    def set_login_time(self):
        self.login_time = self.set_time()
