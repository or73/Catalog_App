"""
File Path: application/modules/item/methods.py
Description: Item methods for App - Define Item methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
# Methods
from catalog.methods import CatalogMethod
# from category.methods import CategoryMethod
# Models
from category.models import Category
from .models import Item
# DB
from setup import db


class ItemMethod:
    @staticmethod
    def create_item(name, description, price, owner):
        """
        Create function, which receives a JSON object'
        and creates a new Item in the database, extracting all
        of the fields required to populate it with the information
        gathered from the 'session'
        It then return the 'item.id' of the new created Item.
        :param name: Item name
        :param description: Item description
        :param price: Item price
        :param owner: Item owner
        :return: item.id
        """
        print('-------------------- Item - create_item')
        new_item = Item(name=name,
                        description=description,
                        price=price,
                        owner=owner)
        db.session.add(new_item)
        db.session.commit()
        # Validate if user was created
        item = Item.query.filter_by(name=name).first()
        if item:
            return item
        else:
            return 'Item could not be created'

    @staticmethod
    def get_item(item_id):
        print('------------------ Item - get_item by id')
        return Item.query.filter_by(id=item_id).first()

    @staticmethod
    def get_item_name(item_name):
        print('------------------ get_item by name')
        return Item.query.filter_by(name=item_name).first()

    @staticmethod
    def get_all_items_by_provided_ids(items_ids):
        print('------------------ Item - get_all_items_by_provided_ids')
        items_name_list = []
        for item_id in items_ids:
            item = Item.query.filter_by(id=item_id).one()
            items_name_list.append(item.get_name())
        return items_name_list

    @staticmethod
    def get_all_items_ids_by_provided_names(items_name):
        print('------------------ Item - get_all_items_ids_by_provided_names')
        items_id_list = []
        for item_name in items_name:
            item = Item.query.filter_by(name=item_name).first()
            items_id_list.append(item.get_id())
        return items_id_list

    @staticmethod
    def get_all_items(order_type):
        print('------------------ Item - get all items')
        if order_type == 'asc':
            return Item.query.order_by(Item.name).all()
        elif order_type == 'desc':
            return Item.query.order_by(Item.name.desc()).all()
        return None

    @staticmethod
    def get_all_items_name():
        all_items_list = Item.query.with_entities(Item.name)
        return all_items_list

    @staticmethod
    def get_id_by_name(item_name):
        print('------------------ Item - get_id_by_name - %s' % item_name)
        item = Item.query.filter_by(name=item_name).first()
        return item.get_id()

    #@staticmethod
    #def get_id_list_by_provided_name_list(new_items):
    #    print('--------------- Item - get_id_list_by_provided_name_list')
    #    item_id_list = []
    #    for new_item_name in new_items:
    #        item = Item.query.filter_by(name=new_item_name).first()
    #        item_id_list.append(item.get_id())
    #    return item_id_list

    @staticmethod
    def get_id_list_by_provided_name_list(new_categories):
        print('--------------- Category - get_id_list_by_provided_name_list')
        category_id_list = []
        for new_category_name in new_categories:
            category = Category.query.filter_by(name=new_category_name).first()
            category_id_list.append(category.get_id())
        return category_id_list

    @staticmethod
    def get_owner_by_name(item_name):
        print('------------------ item (%s) - get_owner' % item_name)
        item = Item.query.filter_by(name=item_name).first()
        if item:
            print(
                'Item %s has been found, and his own is user with id: %s' % (item_name, item.get_user_id()))
        else:
            print('Item %s could not be found' % item_name)
        return item.get_user_id()

    @staticmethod
    def set_name(item_name):
        item = Item.query.filter_by(name=item_name).first()
        if item: 
            item.set_name(item_name)
            item.set_last_update()
            db.commit()
            return True
        return False

    @staticmethod
    def set_description(item_id, item_description):
        item = Item.query.filter_by(id=item_id).first()
        if item:
            item.set_description(item_description)
            item.set_last_update()
            db.commit()
            return True
        return False

    @staticmethod
    def set_price(item_id, item_price):
        item = Item.query.filter_by(id=item_id).first()
        if item:
            item.set_price(item_price)
            item.set_last_update()
            db.commit()
            return True
        return False

    @staticmethod
    def delete(item_id):
        print('------------------- Item - delete: item_id: %s' % item_id)
        item = Item.query.filter_by(id=item_id).first()
        current_db_session = db.session.object_session(item)
        current_db_session.delete(item)
        current_db_session.commit()

    @staticmethod
    def update_item(item_id, new_name, new_description, new_price, new_categories):
        """ update_item returns a list of deleted categories or empty if none was deleted,
               and a list of new categories or empty if nones was added
        :param item_id: item_id
        :param new_name: New Item name
        :param new_description: New Item description
        :param new_price: New Item price
        :param new_categories: updated Item categories list (items name)
        """
        item = ItemMethod.get_item(item_id)
        """ Item to be modified/updated """

        """ Compare & Update 'name', 'description' & 'price' data """
        if item.get_name() != new_name:
            item.set_name(new_name)
            db.session.merge(item)
            db.session.commit()
        if item.get_description() != new_description:
            item.set_description(new_description)
            db.session.merge(item)
            db.session.commit()
        if item.get_price() != new_price:
            item.set_price(new_price)
            db.session.merge(item)
            db.session.commit()

        # new_categories_id_list = CategoryMethod.get_id_list_by_provided_name_list(new_categories)
        new_categories_id_list = ItemMethod.get_id_list_by_provided_name_list(new_categories)
        """ Create list of item id from list of item name """
        CatalogMethod.update_catalog(item_id, new_categories_id_list, 'item')
        """ Update Catalog """

        # new_items_id_list = ItemMethod.get_id_list_by_provided_name_list(new_items)
        # """ Create list of item id from list of item name """
        # CatalogMethod.update_catalog(category_id, new_items_id_list, 'category')
        # """ Update Catalog """
