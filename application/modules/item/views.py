"""
File Path: application/modules/item/views.py
Description: Item routes/paths for App - Define Item routes/paths
Copyright (c) 2019. This Application has been developed by OR73.
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

# Methods
from auth.methods import AuthMethod
from catalog.methods import CatalogMethod
from category.methods import CategoryMethod
from item.methods import ItemMethod
# Models
from catalog.models import Catalog
from item.models import Item
# DB
from setup import db

item_bp = Blueprint('item_bp', __name__)


@item_bp.route('/item/<string:item_name>/')
def show_item(item_name):
    """Public route - shows Item detailed information"""
    print('---------------- Item - show_item')
    # Validate if the Item provided exists in DB
    item = Item.query.filter_by(name=item_name).first()
    if item:
        print('The Item %s exist' % item_name)
        # Get all categories of an Item
        categories = CatalogMethod.get_all_categories_of_item_id(item.get_id())
        return render_template('item/show_item.html',
                               title=item_name,
                               subtitle='Item Details',
                               item=item,
                               categories=categories)
    else:
        flash('Required Item (%s) doesn\'t exist')
        return redirect(url_for('catalog_bp.index'))


@item_bp.route('/item/new/', methods=['GET', 'POST'])
@login_required
def create():
    print('---------------- Item - create_item - %s' % request.method)
    if request.method == 'GET':
        categories = CategoryMethod.get_all_categories('asc')
        return render_template('item/create_item.html', categories=categories)
    elif request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        categories_selected = request.form.getlist('category_list')
        print('name: ', name)
        print('description: ', description)
        print('price: ', price)
        print('categories_selected: ', categories_selected)

        # Create new item
        ItemMethod.create_item(name=name,
                               description=description,
                               price=price,
                               owner=AuthMethod.get_current_user_id())
        # Add items to Category
        for category in categories_selected:
            new_catalog = Catalog(category_id=CategoryMethod.get_id_by_name(category),
                                  item_id=ItemMethod.get_id_by_name(name))
            db.session.add(new_catalog)
            db.session.commit()
        flash('New Item (%s) has been created successfully' % name)
        return redirect(url_for('catalog_bp.index'))

    flash('Required operation is not authorized')
    return redirect(url_for('catalog_bp.index'))


@item_bp.route('/item/edit/<string:item_name>', methods=['GET', 'POST'])
@login_required
def edit(item_name):
    print('----------------- Category - edit - %s' % request.method)
    item = ItemMethod.get_item_name(item_name)

    """ Validate if current_user is the owner of item_name """
    item_owner_db_id = ItemMethod.get_owner_by_name(item_name)
    current_session_user_id = AuthMethod.get_current_user_id()

    if item_owner_db_id == current_session_user_id:
        """ Load item to be edited """
        item_categories = CatalogMethod.get_all_categories_of_item_id(item.get_id())
        print('item_categories: ', item_categories)
        """ Retrieve all categories associated with current Item """
        categories = CategoryMethod.get_all_categories_name()
        print('categories: ', categories)
        """ Retrieve all Items in DB """

        if request.method == 'GET':
            return render_template('item/edit_item.html',
                                   item=item,
                                   item_categories=item_categories,
                                   categories=categories,
                                   title='Edit Item - %s' % item_name)
        elif request.method == 'POST':
            new_name = request.form.get('name')
            new_description = request.form.get('description')
            new_price = request.form.get('price')
            new_categories_selected = request.form.getlist('item_list')

            item_id = ItemMethod.get_id_by_name(item_name)
            print('-------------*********** item_id: ', item_id)
            # Update new Item
            ItemMethod.update_item(item_id=item_id,
                                   new_name=new_name,
                                   new_description=new_description,
                                   new_price=new_price,
                                   new_categories=new_categories_selected)
            """ update_item """

            flash('New Item (%s) has been created successfully' % new_name)
            return redirect(url_for('catalog_bp.index'))
    else:
        flash('Current user is not owner of selected Item...')
        return redirect(url_for('catalog_bp.index'))


@item_bp.route('/item/delete/<string:item_name>', methods=['GET'])
@login_required
def delete(item_name):
    print('----------------- Item - delete - %s' % request.method)

    """ Validate if current_user is the owner of item_name """
    item_owner_db_id = ItemMethod.get_owner_by_name(item_name)
    current_session_user_id = AuthMethod.get_current_user_id()

    if item_owner_db_id == current_session_user_id:
        """ Load item to be edited """
        print('Item - delete - GET')
        item_id = ItemMethod.get_id_by_name(item_name)
        """ item_id by provided item_name """
        categories_id_of_item = CatalogMethod.get_all_categories_id_of_item_id(item_id)
        """ All categories_id of a item_id """
        ItemMethod.delete(item_id)
        """ Delete Item """
        CatalogMethod.delete_list_of_item_categories(item_id, categories_id_of_item)
        """ Delete all links of items with a specified item_id """
        return redirect(url_for('catalog_bp.index'))
    else:
        flash('Current user is not owner of selected Item...')
        return redirect(url_for('catalog_bp.index'))

# ------------- Falta validar las operaciones cuando 'Category', 'Item', 'Catalog' y 'Auth' ya existen en la BD
