"""
File Path: application/modules/user/views.py
Description: User routes/paths for App - Define user routes/paths
Copyright (c) 2019. This Application has been developed by OR73.
"""
import json
from flask import Blueprint, flash, jsonify, make_response, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
# --------------- DataBase
from sqlalchemy.exc import SQLAlchemyError
# --------------- HTTP Authorization
from flask_httpauth import HTTPBasicAuth
from flask import g

# Models
from .models import User
# DB
from setup import db

user_bp = Blueprint('user_bp', __name__)


def mk_response(message, code, c_type):
    response = make_response(json.dumps(message), code)
    response.headers['Content-type'] = c_type
    return response


@user_bp.route('/user/create/<user_data>/')
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
                    username=user_data['username'])
    db.session.add(new_user)
    db.session.commit()
    # Validate if user was created
    user = User.query.filter_by(email=user_data['email']).first()
    if user:
        return user.id
    else:
        return 'User could not be created'
