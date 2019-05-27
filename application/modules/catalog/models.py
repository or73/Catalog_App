"""
File Path: application/modules/catalog/models.py
Description: Catalog models for App - Define Catalog models
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime

from setup import db
from crud import CRUDMixin


class Catalog(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Category
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'))
    # Item
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete='CASCADE'))
    # Catalog Control
    last_update = db.Column(db.DateTime())

    def __init__(self, category_id, item_id):
        self.category_id = category_id
        self.item_id = item_id
        self.last_update = self.set_time()

    @staticmethod
    def set_time():
        return datetime.datetime.now()

    def get_category_id(self):
        return self.category_id

    def get_item_id(self):
        return self.item_id

    def get_last_update(self):
        return self.last_update

    def set_category_id(self, category_id):
        self.category_id = category_id

    def set_item_id(self, item_id):
        self.item_id = item_id

    def set_last_update(self):
        self.last_update = self.set_time()
