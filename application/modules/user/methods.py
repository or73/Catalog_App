"""
File Path: application/modules/user/methods.py
Description: User methods for App - Define User methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
# --------------- DataBase
from sqlalchemy.exc import SQLAlchemyError
# --------------- HTTP Authorization
from flask_httpauth import HTTPBasicAuth
from flask import g

# Methods
from auth.methods import AuthMethod
# Models
from .models import User
# DB
from setup import db


class UserMethod:
    @staticmethod
    def create_user(user_data):
        """
        Create 'createUser' function, which receives a 'session'
        and creates a new user in the database, extracting all
        of the fields required to populate it with the information
        gathered from the 'session'.
        It then return the 'user.id' of the new created user.
        :param user_data: User data
        :return: user.id
        """
        print('-------------------- create_user')
        print('user_data: ', user_data)
        new_user = User(authenticated=user_data['authenticated'],
                        email=user_data['email'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        password=user_data['password'],
                        picture=user_data['picture'],
                        profile=user_data['profile'],
                        provider=user_data['provider'],
                        session_token=user_data['session_token'],
                        username=user_data['username'])
        db.session.add(new_user)
        db.session.commit()
        # Validate if user was created
        user = User.query.filter_by(email=user_data['email']).first()
        if user:
            return user.id
        else:
            return 'User could not be created'

    @staticmethod
    def get_user(email):
        """
        Search a user by its provided email, and if the user exists in the DB, then
        User object is returned
        :param email: user email
        :return: User Object if user exists or None if does not exist
        """
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                return user
            else:
                return False
        except SQLAlchemyError:
            return None

    @staticmethod
    def get_user_id(email):
        """
        Search a user by its provided email, and if the user exists in the DB, then
        user._id is returned
        :param email: user email
        :return: user.id if user exists or None if does not exist
        """
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                return user.get_id()
            else:
                return False
        except SQLAlchemyError:
            return None

    @staticmethod
    def get_user_id_session_token(session_token):
        user = User.query.filter_by(session_token=session_token).first()
        if user:
            return user.id
        else:
            return None

    @staticmethod
    def get_user_info_id(user_id):
        """
        Find a user searching in DB by its provided user_id
        :param user_id: user id to search in DB
        :return: user data
        """
        user = User.query.filter_by(id=user_id).first()
        return user

    @staticmethod
    def get_user_info_name(user_name):
        """
        Find a user searching in DB by its provided username
        :param user_name: user name to search in DB
        :return: user data
        """
        user = User.query.filter_by(username=user_name).first()
        return user

    @staticmethod
    def get_user_session_token(session_token):
        return User.query.filter_by(session_token=session_token).first()

    @staticmethod
    def validate_owner(user_id):
        owner = User.query.filter_by(id=AuthMethod.get_current_user_id()).first()
        return owner == user_id
