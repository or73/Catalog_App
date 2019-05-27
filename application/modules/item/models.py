"""
File Path: application/modules/item/models.py
Description: Item models for App - Define Item models
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime

from setup import db
from crud import CRUDMixin


class Item(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Item
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text())
    price = db.Column(db.String())

    # Owner
    user_id = db.Column(db.Integer)

    # Catalog Control
    last_update = db.Column(db.DateTime, default=datetime.datetime.now())

    # ---------------------------------------------------------------------

    def __init__(self, name, description, price, owner):
        # Item fields
        self.name = name
        self.description = description
        self.price = price
        # Item control
        self.set_last_update()
        # Owner
        self.user_id = owner

    # ----------------------------- GETTERS ---------------------------------
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_price(self):
        return self.price

    def get_last_update(self):
        return self.last_update

    def get_user_id(self):
        return self.user_id

    # ----------------------------- SETTERS ---------------------------------
    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_price(self, price):
        self.price = price

    def set_last_update(self):
        self.last_update = datetime.datetime.now()

    def set_user_id(self, user_id):
        self.user_id = user_id
