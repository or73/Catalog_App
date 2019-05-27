"""
File Path: application/modules/category/methods.py
Description: Category methods for App - Define Category methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
from setup import db
from .models import Category
from catalog.methods import CatalogMethod
# from item.methods import ItemMethod
from item.models import Item


class CategoryMethod:
    @staticmethod
    def create_category(name, description, owner):
        """
        Create function, which receives a JSON object'
        and creates a new Category in the database, extracting all
        of the fields required to populate it with the information
        gathered from the 'session'
        It then return the 'category.id' of the new created Category.
        :param name: Category name
        :param description: Category description
        :param owner: Category owner
        :return: category.id
        """
        print('-------------------- create_category')
        new_category = Category(name=name,
                                description=description,
                                owner=owner)
        db.session.add(new_category)
        db.session.commit()
        # Validate if user was created
        category = Category.query.filter_by(name=name).first()
        if category:
            return category
        else:
            return 'Category could not be created'

    @staticmethod
    def get_category(cat_id):
        print('------------------ category - get_category by id')
        return Category.query.filter_by(id=cat_id).first()

    @staticmethod
    def get_category_name(cat_name):
        print('------------------ category - get_category by name')
        return Category.query.filter_by(name=cat_name).first()

    @staticmethod
    def get_all_categories(order_type):
        print('------------------ category - get all categories')
        if order_type == 'asc':
            return Category.query.order_by(Category.name).all()
        elif order_type == 'desc':
            return Category.query.order_by(Category.name.desc()).all()
        return None

    @staticmethod
    def get_all_categories_by_provided_ids(categories_ids):
        print('------------------ category - get all categories_by_provided_ids')
        categories_name_list = []
        for category_id in categories_ids:
            category = Category.query.filter_by(id=category_id).one()
            categories_name_list.append(category.get_name())
        return categories_name_list

    @staticmethod
    def get_id_by_name(category_name):
        print('------------------ Category - get_id_by_name')
        category = Category.query.filter_by(name=category_name).first()
        return category.get_id()

    @staticmethod
    def get_owner_by_name(category_name):
        print('------------------ category (%s) - get_owner' % category_name)
        category = Category.query.filter_by(name=category_name).first()
        if category:
            print('Category %s has been found, and his own is user with id: %s' %
                  (category_name, category.get_user_id()))
        else:
            print('Category %s could not be found' % category_name)
        return category.get_user_id()

    @staticmethod
    def get_all_categories_name():
        all_categories_list = Category.query.with_entities(Category.name)
        return all_categories_list

    #@staticmethod
    #def get_id_list_by_provided_name_list(new_categories):
    #    print('--------------- Category - get_id_list_by_provided_name_list')
    #    category_id_list = []
    #    for new_category_name in new_categories:
    #        category = Category.query.filter_by(name=new_category_name).first()
    #        category_id_list.append(category.get_id())
    #    return category_id_list
    @staticmethod
    def get_id_list_by_provided_name_list(new_items):
        print('--------------- Item - get_id_list_by_provided_name_list')
        item_id_list = []
        for new_item_name in new_items:
            item = Item.query.filter_by(name=new_item_name).first()
            item_id_list.append(item.get_id())
        return item_id_list

    @staticmethod
    def set_name(cat_name):
        print('------------------ category - set name')
        category = Category.query.filter_by(name=cat_name).first()
        if category:
            category.set_name(cat_name)
            category.set_last_update()
            db.commit()
            return True
        return False

    @staticmethod
    def set_description(cat_id, cat_description):
        print('------------------ category - set description')
        category = Category.query.filter_by(id=cat_id).first()
        if category:
            category.set_description(cat_description)
            category.set_last_update()
            db.commit()
            return True
        return False

    @staticmethod
    def delete(category_id):
        print('------------------- Category - delete: category_id: %s' % category_id)
        category = Category.query.filter_by(id=category_id).first()
        current_db_session = db.session.object_session(category)
        current_db_session.delete(category)
        current_db_session.commit()

    @staticmethod
    def update_category(category_id, new_name, new_description, new_items):
        """ update_category returns a list of deleted items or empty if none was deleted,
               and a list of new items or empty if nones was added
        :param category_id: Category_id
        :param new_name: New Category name
        :param new_description: New Category description
        :param new_items: updated Category Items list (items name)
        """
        category = CategoryMethod.get_category(category_id)
        """ Category to be modified/updated """

        """ Compare & Update 'name' & 'description' data """
        if category.get_name() != new_name:
            category.set_name(new_name)
            db.session.merge(category)
            db.session.commit()
        if category.get_description() != new_description:
            category.set_description(new_description)
            db.session.merge(category)
            db.session.commit()

        # new_items_id_list = ItemMethod.get_id_list_by_provided_name_list(new_items)
        new_items_id_list = CategoryMethod.get_id_list_by_provided_name_list(new_items)
        """ Create list of item id from list of item name """
        CatalogMethod.update_catalog(category_id, new_items_id_list, 'category')
        """ Update Catalog """
