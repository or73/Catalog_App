"""
File Path: application/modules/auth/methods.py
Description: Auth methods for App - Define auth/login methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
from flask_login import current_user
import datetime

from setup import db
from .models import Auth
from user.models import User


class AuthMethod:
    @staticmethod
    def create_auth(user_id):
        """
        Create 'createUser' function, which receives a 'session'
        and creates a new user in the database, extracting all
        of the fields required to populate it with the information
        gathered from the 'session'.
        It then return the 'user.id' of the new created user.
        :param user_id: User id
        :return: auth
        """
        print('-------------------- create_auth')
        new_auth = Auth(user_id=user_id)
        db.session.add(new_auth)
        db.session.commit()
        auth = Auth.query.filter_by(user_id=user_id).first()
        if auth:
            return auth
        else:
            return None

    @staticmethod
    def get_all():
        """ Return a dictionary with username, login/logout time in specific format & duration time"""
        all_auth = Auth.query.order_by(Auth.user_id).all()
        """ All auth login/logout events """
        login_logout = {}
        for auth in all_auth:
            auth_user = User.query.filter_by(id=auth.user_id).first()
            login = auth.get_login_time()
            if auth.logout_time is not None:
                logout = auth.get_logout_time()
                duration = logout - login
            else:
                logout = None
                duration = datetime.datetime.now() - login

            login_logout[auth_user.get_username()] = {'login': login, 'logout': logout, 'duration': duration }
        return login_logout

    """
    @staticmethod
    def get_all_links_group_by_category():
        all_categories = Category.query.order_by(Category.name).all()
        "" All categories""
        links_by_category = {}
        for category in all_categories:
            category_items_id = CatalogMethod.get_all_items_id_of_category_id(category.get_id())
            "" All items_id of a category ""
            links_by_category[category.get_name()] = []
            for item_id in category_items_id:
                item = Item.query.filter_by(id=item_id).first()
                links_by_category[category.get_name()].append(item.get_name())
        return links_by_category
    """

    @staticmethod
    def get_login_time(user_id):
        return Auth.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_logout_time(user_id):
        return Auth.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_all_login_time(user_id):
        return Auth.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_all_logout_time(user_id):
        return Auth.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_all_login_users_of_period_of_time(start_time, end_time):
        return Auth.query.filter(Auth.login_time >= start_time, Auth.login_time <= end_time).all()

    @staticmethod
    def get_all_logout_users_of_period_of_time(start_time, end_time):
        return Auth.query.filter(Auth.logout_time >= start_time, Auth.logout_time <= end_time).all()

    @staticmethod
    def get_current_user_id():
        if current_user.id:
            print('current_user.id: ', current_user.id)
            return current_user.id
        print('current_user: ', current_user)
        return current_user
