"""
    JSON endpoints for the item catalog project.
"""


from flask import jsonify, redirect, url_for, flash
from sqlalchemy.orm.exc import NoResultFound

from sportsbazar import app
from sportsbazar.db_setup import Category, Item
from sportsbazar.db_connect import db_connect


@app.route('/catalog/JSON')
@app.route('/catalog.json')
def categoryJSON():
    session = db_connect()
    categories = session.query(Category).all()
    return jsonify(Categories=[cat.serialize for cat in categories])


@app.route('/catalog/<category_name>/JSON')
def categoryItemsJSON(category_name):
    session = db_connect()
    category = session.query(Category).filter_by(name=category_name).one()
    return jsonify(category=category.serialize)


@app.route('/catalog/<category_name>/<item_name>/JSON')
def itemJSON(item_name, category_name=None):
    session = db_connect()
    item = session.query(Item).filter_by(name=item_name).one()
    return jsonify(Item=item.serialize)
# End JSON Endpoints
