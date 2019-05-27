"""
File Path: application/modules/catalog/methods.py
Description: Catalog methods for App - Define Catalog methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime
from setup import db
from .models import Catalog
from category.models import Category
from item.models import Item


class CatalogMethod:
    @staticmethod
    def create_catalog(catalog_data):
        """
        Create function, which receives a JSON object'
        and creates a new Catalog in the database, extracting all
        of the fields required to populate it with the information
        gathered from the 'session'
        It then return the 'catalog.id' of the new created Catalog.
        :param catalog_data: Catalog data
        :return: catalog.id
        """
        print('-------------------- create_catalog')
        print('catalog_data: ', catalog_data)
        print('catalog_data[category_id]: ', catalog_data['category_id'])
        print('catalog_data[item_id]: ', catalog_data['item_id'])
        new_catalog = Catalog(category_id=catalog_data['category_id'],
                              item_id=catalog_data['item_id'])
        db.session.add(new_catalog)
        db.session.commit()
        # Validate if user was created
        catalog = Catalog.query.filter_by(category_id=catalog_data['category_id'],
                                          item_id=catalog_data['item_id']).first()
        db.session.remove()
        if catalog:
            return catalog.id
        else:
            return 'Catalog could not be created'

    @staticmethod
    def get_all_links_group_by_category():
        all_categories = Category.query.order_by(Category.name).all()
        """ All categories"""
        links_by_category = {}
        for category in all_categories:
            category_items_id = CatalogMethod.get_all_items_id_of_category_id(category.get_id())
            """ All items_id of a category """
            links_by_category[category.get_name()] = []
            for item_id in category_items_id:
                item = Item.query.filter_by(id=item_id).first()
                links_by_category[category.get_name()].append(item.get_name())
        return links_by_category

    @staticmethod
    def get_all_links_group_by_item():
        all_items = Item.query.order_by(Item.name).all()
        """ All Items """
        links_by_item = {}
        for item in all_items:
            items_category_id = CatalogMethod.get_all_categories_id_of_item_id(item.get_id())
            """ All categories_id of an Item """
            links_by_item[item.get_name()] = []
            for category_id in items_category_id:
                category = Category.query.filter_by(id=category_id).first()
                links_by_item[item.get_name()].append(category.get_name())
        return links_by_item

    @staticmethod
    def get_catalog(cat_id):
        print('------------------ get_catalog by id')
        return Catalog.query.filter_by(id=cat_id).first()

    @staticmethod
    def get_all_categories_id():
        print('------------------ get_all_categories_id')
        return Catalog.query.with_entities(Catalog.category_id)

    @staticmethod
    def get_all_items_id():
        print('------------------ get_all_items_id')
        return Catalog.query.with_entities(Catalog.item_id)

    @staticmethod
    def get_all_items_of_category_id(category_id):
        print('------------------ get_all_items_of_category_id')
        all_items_list = list(Catalog.query.filter_by(category_id=category_id).with_entities(Catalog.item_id))
        items_list_to_return = [(Item.query
                                 .filter_by(id=x[0])
                                 .first()).get_name() for x in all_items_list]
        """ Return a list of Items names of an specified Category """
        return items_list_to_return

    @staticmethod
    def get_all_categories_of_item_id(item_id):
        print('------------------ get_all_categories_of_item_id')
        all_categories_list = list(Catalog.query.filter_by(item_id=item_id).with_entities(Catalog.category_id))
        categories_list_to_return = [(Category.query
                                      .filter_by(id=x[0])
                                      .first()).get_name() for x in all_categories_list]
        """ Return a list of Categories of an specified Item """
        return categories_list_to_return

    @staticmethod
    def get_all_items_id_of_category_id(category_id):
        print('---------------- Catalog - get_all_items_id_of_category_id')
        list_of_items_id = list(Catalog.query.filter_by(category_id=category_id).with_entities(Catalog.item_id))
        items_id_list = []
        for item_duple in list_of_items_id:
            items_id_list.append(item_duple[0])
        return items_id_list

    @staticmethod
    def get_all_categories_id_of_item_id(item_id):
        print('---------------- Catalog - get_all_categories_id_of_item_id')
        list_of_categories_id = list(Catalog.query.filter_by(item_id=item_id).with_entities(Catalog.category_id))
        categories_id_list = []
        for item_duple in list_of_categories_id:
            categories_id_list.append(item_duple[0])
        return categories_id_list

    @staticmethod
    def update_catalog(category_item_id, new_categories_items_id_list, category_or_item):
        """
        Update items of a Category
        :param category_item_id: Category_id or Item_id
        :param new_categories_items_id_list:  list of item id's to add to current Category
                or list of category id's to add to current Item
        :param category_or_item: string that identifies if is an update of category or item
        :return: None
        """

        print('------------------ Catalog - update_catalog: %s' % category_or_item)
        current_category_items = []
        if category_or_item == 'category':
            current_category_items = CatalogMethod.get_all_items_id_of_category_id(category_item_id)
            """ Current Category Items """

        elif category_or_item == 'item':
            current_category_items = CatalogMethod.get_all_categories_id_of_item_id(category_item_id)
            """ Current Item Categories """

        categories_items_id_list_to_add = []
        for new_category_item_id in new_categories_items_id_list:
            if new_category_item_id not in current_category_items:
                categories_items_id_list_to_add.append(new_category_item_id)
        """ Validate if 'new_categories_items_id_list' contains any new item, 
                making a comparison between new_categories_items_id_list and 
               'current_category_items' """

        categories_items_id_list_to_delete = []
        for current_category_item_id in current_category_items:
            if current_category_item_id not in new_categories_items_id_list:
                categories_items_id_list_to_delete.append(current_category_item_id)
        """ Validate if 'new_categories_items_id_list' does not contains some of the 'current_category_items' """

        if len(categories_items_id_list_to_add) > 0:
            print('items_id_list_to_add :', categories_items_id_list_to_add)
            if category_or_item == 'category':
                for item_id in categories_items_id_list_to_add:
                    CatalogMethod.add(category_item_id, item_id)
                """ Add new item-category link to Catalog """
            if category_or_item == 'item':
                for category_id in categories_items_id_list_to_add:
                    CatalogMethod.add(category_id, category_item_id)
                """ Add new item-category link to Catalog """
        """ If 'categories_items_list_to_add' contains one or more items, 
               then add item-category link to Catalog """

        if len(categories_items_id_list_to_delete) > 0:
            print('items_id_list_to_delete: ', categories_items_id_list_to_delete)
            if category_or_item == 'category':
                for item_id in categories_items_id_list_to_delete:
                    CatalogMethod.delete(category_item_id, item_id)
                """ Delete item-category link from Catalog"""
            if category_or_item == 'item':
                for category_id in categories_items_id_list_to_delete:
                    CatalogMethod.delete(category_id, category_item_id)
        """ If 'categories_items_list_to_delete' contains one or more items, 
               then delete item-category link from Catalog """

    @staticmethod
    def delete_list_of_category_items(category_id, items_id_of_category):
        print('--------------- Catalog - delete_list_of_category_items ')
        for item_id in items_id_of_category:
            link_to_delete = Catalog.query.filter_by(category_id=category_id, item_id=item_id).first()
            current_db_session = db.session.object_session(link_to_delete)
            current_db_session.delete(link_to_delete)
            current_db_session.commit()

    @staticmethod
    def delete_list_of_item_categories(item_id, categories_id_of_item):
        print('--------------- Catalog - delete_list_of_item_categories ')
        for category_id in categories_id_of_item:
            link_to_delete = Catalog.query.filter_by(category_id=category_id, item_id=item_id).first()
            current_db_session = db.session.object_session(link_to_delete)
            current_db_session.delete(link_to_delete)
            current_db_session.commit()

    @staticmethod
    def add(category_id, item_id):
        print('---------------- Catalog - add: category_id: %s - item_id: %s' % (category_id, item_id))
        link_to_add = Catalog(category_id, item_id)
        db.session.add(link_to_add)
        db.session.commit()

    @staticmethod
    def delete(category_id, item_id):
        print('---------------- Catalog - delete: category_id: %s - item_id: %s' % (category_id, item_id))
        link_to_delete = Catalog.query.filter_by(category_id=category_id, item_id=item_id).first()
        current_db_session = db.session.object_session(link_to_delete)
        current_db_session.delete(link_to_delete)
        current_db_session.commit()

    @staticmethod
    def get_all_links_names_by_category():
        """ All catalog_links with category_name & item_name, grouped by category """
        # { category_name: [items], ... }
        print('---------------- Catalog - get_all_links_names_by_category')

        """ All catalog_links with category_id & item_id """
        return CatalogMethod.get_all_links_group_by_category()

    @staticmethod
    def get_all_links_names_by_item():
        """ All catalog_links with category_name & item_name, grouped by item """
        # { item_name: [categories], ... }
        print('---------------- Catalog - get_all_links_names_by_id')
        """ All catalog_links with category_id & item_id """
        return CatalogMethod.get_all_links_group_by_item()

    @staticmethod
    def get_all_login_logout_sessions_names():
        """ All login_logout_sessions start/end with date-format & time duration """
        return None
