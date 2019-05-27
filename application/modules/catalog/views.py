"""
File Path: application/modules/catalog/views.py
Description: Catalog routes/paths for App - Define Catalog routes/paths
Copyright (c) 2019. This Application has been developed by OR73.
"""
import os
from flask import Blueprint, flash, redirect, render_template, request, url_for, send_from_directory
from flask_login import current_user, login_required, login_user, logout_user

from auth.methods import AuthMethod
from catalog.methods import CatalogMethod
from category.methods import CategoryMethod
from item.methods import ItemMethod

catalog_bp = Blueprint('catalog_bp', __name__)


@catalog_bp.route('/')
@catalog_bp.route('/catalog')
def index():

    # categories = Category.query(name).distinct().order_by(desc(name))
    # items = Item.query().all()
    # return render_template('index.html', categories=categories, items=items, item_categories=item_categories)

    # Load all categories from DB
    categories = CategoryMethod.get_all_categories('asc')
    # Load all items from DB
    items = ItemMethod.get_all_items('asc')
    # Load all categories in which the same item exist
    item_categories = {}
    for item in items:
        item_categories[item.get_name()] = CatalogMethod.get_all_categories_of_item_id(item.get_id())

    return render_template('index.html',
                           title='Catalog Application',
                           subtitle='Python3 + Flask + SQLALchemy',
                           categories=categories,
                           item_categories=item_categories)


@catalog_bp.route('/endpoint')
@login_required
def endpoint():
    """ Run and display various analytics reports """
    categories = CategoryMethod.get_all_categories('asc')
    """ All categories is ascendant order """

    items = ItemMethod.get_all_items('asc')
    """ All items in ascendant order """

    # { category_name: [items_name ], ... }
    catalog_links_name_by_category = CatalogMethod.get_all_links_names_by_category()
    """ All catalog_links with category_name & item_name, grouped by category """
    # { item_name: [categories_name ], ... }
    catalog_links_name_by_item = CatalogMethod.get_all_links_names_by_item()
    """ All catalog_links with category_name & item_name, grouped by item """

    # { user_id: [(login_time, logout_time), ...], ... }
    login_logout_sessions = AuthMethod.get_all()
    """ All login_logout_sessions start/end """

    print('login_logout_sessions: ', login_logout_sessions)

    # user_name - login_time - logout_time - duration
    # login_logout_sessions_name = CatalogMethod.get_all_login_logout_sessions_names()
    """ All login_logout_sessions start/end with date-format & time duration """
    return render_template('catalog/endpoint.html',
                           title='EndPoint',
                           categories=categories,
                           items=items,
                           catalog_links_categories=catalog_links_name_by_category,
                           catalog_links_items=catalog_links_name_by_item,
                           login_logout_sessions=login_logout_sessions)


@catalog_bp.route('/favicon')
@catalog_bp.route('/favicon.ico')
def favicon():
    ico_dir = os.path.join(os.path.dirname(os.getcwd()), 'userApp', 'application', 'static', 'dist', 'img', 'ico')
    print('ico_dir: ', ico_dir)
    return send_from_directory(ico_dir, 'favicon.ico')


@catalog_bp.errorhandler(400)
def key_error(e):
    return render_template('catalog/400.html', error=e), 400


@catalog_bp.errorhandler(500)
def internal_server_error(e):
    return render_template('catalog/generic.html', error=e), 500


@catalog_bp.errorhandler(Exception)
def unhandled_exception(e):
    return render_template('catalog/generic.html', error=e, exception=Exception), 500



