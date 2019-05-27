"""
File Path: application/modules/category/models.py
Description: Category models for App - Define Category models
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime

from setup import db
from crud import CRUDMixin


class Category(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Category
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text())

    # Catalog Control
    last_update = db.Column(db.DateTime(), default=datetime.datetime.now())

    # Owner
    user_id = db.Column(db.Integer)

    # ---------------------------------------------------------------------

    def __init__(self, name, description, owner):
        # Category fields
        self.name = name
        self.description = description
        # Category control
        self.last_update = self.set_time()
        # Owner
        self.user_id = owner

    # ----------------------------- GETTERS ---------------------------------
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_last_update(self):
        return self.last_update

    def get_user_id(self):
        return self.user_id

    # ----------------------------- SETTERS ---------------------------------
    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_last_update(self):
        self.last_update = self.set_time()

    def set_user_id(self, user_id):
        self.user_id = user_id

    @staticmethod
    def set_time():
        return datetime.datetime.now()
