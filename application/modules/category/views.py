"""
File Path: application/modules/category/views.py
Description: Category routes/paths for App - Define Category routes/paths
Copyright (c) 2019. This Application has been developed by OR73.
"""
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from setup import db

# Models
from catalog.models import Catalog
# Methods
from auth.methods import AuthMethod
from catalog.methods import CatalogMethod
from category.methods import CategoryMethod
from item.methods import ItemMethod


category_bp = Blueprint('category_bp', __name__)


@category_bp.route('/category/<string:category_name>/')
def show_category(category_name):
    """Public route - shows Category detailed information"""
    print('--------------- Category - show_category')
    # Validate if the category provided exists in DB
    category = CategoryMethod.get_category_name(category_name)   # Category.query.filter_by(name=category_name).first()
    if category:
        print('The Category %s exist' % category_name)
        # Get all items of category
        items = CatalogMethod.get_all_items_of_category_id(category.get_id())
        return render_template('category/show_category.html',
                               title=category_name,
                               subtitle='Category Details',
                               category=category,
                               items=items)
    else:
        flash('Required category (%s) doesn\'t exist')
        return redirect(url_for('catalog_bp.index'))


@category_bp.route('/category/new/', methods=['GET', 'POST'])
@login_required
def create():
    print('---------------- Category - create_category - %s' % request.method)
    if request.method == 'GET':
        items = ItemMethod.get_all_items('asc')
        return render_template('category/create_category.html', items=items)

    elif request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        items_selected = request.form.getlist('item_list')

        # Create new category
        CategoryMethod.create_category(name=name,
                                       description=description,
                                       owner=AuthMethod.get_current_user_id())
        # Add items to Category
        for item in items_selected:
            new_catalog = Catalog(category_id=CategoryMethod.get_id_by_name(name),
                                  item_id=ItemMethod.get_id_by_name(item))
            db.session.add(new_catalog)
            db.session.commit()
        flash('New Category (%s) has been created successfully' % name)
        return redirect(url_for('catalog_bp.index'))

    flash('Required operation is not authorized')
    return redirect(url_for('catalog_bp.index'))


@category_bp.route('/category/edit/<string:category_name>', methods=['GET', 'POST'])
@login_required
def edit(category_name):
    print('----------------- Category - edit - %s' % request.method)
    category = CategoryMethod.get_category_name(category_name)

    """ Validate if current_user is the owner of category_name """
    category_owner_db_id = CategoryMethod.get_owner_by_name(category_name)
    current_session_user_id = AuthMethod.get_current_user_id()

    if category_owner_db_id == current_session_user_id:
        """ Load category to be edited """
        category_items = CatalogMethod.get_all_items_of_category_id(category.get_id())
        print('category_items: ', category_items)
        """ Retrieve all items associated with current Category """
        items = ItemMethod.get_all_items_name()
        print('items: ', items)
        """ Retrieve all Items in DB """

        if request.method == 'GET':
            return render_template('category/edit_category.html',
                                   category=category,
                                   category_items=category_items,
                                   items=items,
                                   title='Edit Category - %s' % category_name)
        elif request.method == 'POST':
            new_name = request.form.get('name')
            new_description = request.form.get('description')
            new_items_selected = request.form.getlist('item_list')

            category_id = CategoryMethod.get_id_by_name(category_name)
            print('-------------*********** category_id: ', category_id)
            # Update new category
            CategoryMethod.update_category(category_id=category_id,
                                           new_name=new_name,
                                           new_description=new_description,
                                           new_items=new_items_selected)
            """ update_category """

            flash('New Category (%s) has been created successfully' % new_name)
            return redirect(url_for('catalog_bp.index'))
    else:
        flash('Current user is not owner of selected Category...')
        return redirect(url_for('catalog_bp.index'))


@category_bp.route('/category/delete/<string:category_name>', methods=['GET'])
@login_required
def delete(category_name):
    print('----------------- Category - delete - %s' % request.method)

    """ Validate if current_user is the owner of category_name """
    category_owner_db_id = CategoryMethod.get_owner_by_name(category_name)
    current_session_user_id = AuthMethod.get_current_user_id()

    if category_owner_db_id == current_session_user_id:
        """ Load category to be edited """
        print('Category - delete - GET')
        category_id = CategoryMethod.get_id_by_name(category_name)
        """ category_id by provided category_name """
        items_id_of_category = CatalogMethod.get_all_items_id_of_category_id(category_id)
        """ All items_id of a category_id """
        CategoryMethod.delete(category_id)
        """ Delete Category """
        CatalogMethod.delete_list_of_category_items(category_id, items_id_of_category)
        """ Delete all links of items with a specified category_id """
        return redirect(url_for('catalog_bp.index'))
    else:
        flash('Current user is not owner of selected Category...')
        return redirect(url_for('catalog_bp.index'))
