"""
Script to manage the routes / URLs
"""

import os
from flask import render_template, request, redirect, url_for, flash
from flask import send_from_directory
from flask import session as login_session
from sqlalchemy import desc, asc, literal
from sqlalchemy.orm.exc import NoResultFound

from sportsbazar import app
from sportsbazar.db_setup import Category, Item, User
from sportsbazar.db_connect import db_connect
from sportsbazar.auth import getUserId


@app.route('/')
@app.route('/catalog/')
def homepage():
    """
    Shows the Homepage that list the 10 recently added items.
    """
    session = db_connect()
    categories = session.query(Category).order_by(asc(Category.name)).all()
    latest_items = session.query(Item).order_by(desc(Item.id))[0:10]
    session.close()
    return render_template('homepage.html',
                           categories=categories,
                           latest_items=latest_items)


@app.route('/catalog/categories/')
def showCategories():
    """
    Shows all categories.
    """
    session = db_connect()
    categories = session.query(Category).order_by(asc(Category.name)).all()
    if (not categories):
        flash('Warning: No category is added yet.')
    session.close()
    return render_template('categories.html', categories = categories)


@app.route('/catalog/<category_name>/')
def showItems(category_name):
    """
    Shows items in a specific category.

    Args:
        category_name (str): Name of the category to be displayed.

    Returns:
        A web page: showing all the items in the specified category.
        Homepage: if the specified category does not exist.
    """
    session = db_connect()
    # check for invalid category
    try:
        category = session.query(Category).filter_by(name = category_name).one()
    except NoResultFound:
        flash('Error: Category named "%s" is not in the record.' % category_name)
        session.close()
        return redirect(url_for('showCategories'))
    category = session.query(Category).filter_by(name = category_name).one()
    items = session.query(Item).filter_by(category_id = category.id).all()
    if not items:
        flash('Warning: No item is added in this category yet.')
    session.close()
    return render_template('items.html', items = items, category = category)


@app.route('/catalog/<category_name>/<item_name>/')
def showItem(category_name, item_name):
    """
    Shows the details of a particular item from the specified category.

    Args:
        category_name (str): Name of the category to which the item
            belongs.
        item_name (str): Name of the item to be displayed.

    Returns:
        A web page displaying the information of the specified item.
    """
    session = db_connect()
    # check for invalid category
    try:
        category = session.query(Category).filter_by(name = category_name).one()
    except NoResultFound:
        flash('Error: Could not find any category named "%s" in the record.' % category_name)
        session.close()
        return redirect(url_for('showCategories'))
    # check for invalid item
    try:
        item = session.query(Item).filter_by(name = item_name, category_id = category.id).one()
    except NoResultFound:
        flash('Error: No item named "%s" is in "%s" category.' % (item_name, category_name))
        session.close()
        return redirect(url_for('showItems', category_name = category_name))

    user = session.query(User).filter_by(id=item.user_id).one()
    session.close()
    return render_template('item.html', item = item, category = category, user = user)


@app.route('/catalog/myitems/')
def showMyItems():
    """
    Displays the items added by a user.
    """
    if 'username' not in login_session:
        flash('Please sign in to view your items !')
        return redirect(url_for('showLogin'))

    user_id = getUserId(login_session['email'])

    session = db_connect()
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(user_id=user_id).all()
    session.close()
    if not items:
        flash("Warning: You have not added any item yet.")
        return redirect(url_for('homepage'))
    else:
        return render_template('myitems.html', categories=categories, items=items)


@app.route('/catalog/new', methods=['GET', 'POST'])
def newCategory():
    """
    Interface for the user to add a new category.
    """
    if 'username' not in login_session:
        flash('Warning: Please sign in to add new category.')
        return redirect('/login')
    else:
        if login_session['email'] != app.config['ADMIN_EMAIL']:
            flash('Warning: Only admin(s) can add, remove or modify a category.')
            return redirect(url_for('showCategories'))

    if request.method == 'POST':
        session = db_connect()

        # Check for empty name
        if (not request.form['name']) or \
            (request.form['name'].isspace()):
            flash("Error: Category cannot be created with an empty name field.")
            session.close()
            return redirect(url_for('newCategory'))
        # Check for invalid input
        if (request.form['name'].lower() == "categories".lower()):
            # Setting "categories" as category name will cause routing issues
            flash("Error: Route keywords cannot be used as category name(s).")
            session.close()
            return redirect(url_for('newCategory'))

        # Check for duplicate category name
        category = session.query(Category).filter(Category.name == request.form['name'])
        isDuplicate = (session.query(literal(True)).
                          filter(category.exists()).scalar())
        if (isDuplicate):
            flash("Category already exists. "\
                "Please enter a new one.")
            session.close()
            return redirect(url_for('newCategory'))
        else:
            newCategory = Category(name = request.form['name'], user_id=app.config['ADMIN_ID'])
            session.add(newCategory)
            flash('New category "%s" is successfully added.' % newCategory.name)
            session.commit()
            session.close()
            return redirect(url_for('showCategories'))
    else:
        return render_template('newcategory.html')


@app.route('/catalog/<category_name>/edit/', methods=['GET', 'POST'])
def editCategory(category_name):
    """
    Interface for the user to edit a category.

    Args:
    category_name (str): Name of category to be edited.
    """
    if 'username' not in login_session:
        flash('Warning: Please sign in to edit the category.')
        return redirect('/login')
    else:
        if login_session['email'] != app.config['ADMIN_EMAIL']:
            flash('Warning: Only admin(s) can add, remove or modify a category.')
            return redirect(url_for('showCategories'))


    session = db_connect()
    # check for invalid category
    try:
        categoryToEdit = session.query(Category).filter_by(name = category_name).one()
    except NoResultFound:
        flash('Error: Could not find any category named "%s" in the record.' % category_name)
        session.close()
        return redirect(url_for('showCategories'))

    if (request.method == 'POST'):
        # Check for empty name
        if (not request.form['name']) or \
            (request.form['name'].isspace()):
            flash("Error: Category cannot be created with an empty name field.")
            session.close()
            return render_template('editcategory.html', category = categoryToEdit)

        # Check for invalid input
        if (request.form['name'].lower() == "categories".lower()):
            # Setting "categories" as category name will cause routing issues
            flash("Error: Route keywords cannot be used as category name(s).")
            session.close()
            return render_template('editcategory.html', category = categoryToEdit)

        # Check for self duplicate -- not much needed though
        if (request.form['name'] == categoryToEdit.name):
            flash("Error: Modify to new value or cancel")
            session.close()
            return render_template('editcategory.html', category = categoryToEdit)

        # Check for duplicate with category name
        category = session.query(Category).filter(Category.name == request.form['name'])
        isDuplicate = (session.query(literal(True)).
                          filter(category.exists()).scalar())
        if (isDuplicate):
            flash("Error: Category already exists. "\
                "Please enter a new one.")
            session.close()
            return render_template('editcategory.html', category = categoryToEdit)
        else:
            categoryToEdit.name = request.form['name']
            editedCategoryName = categoryToEdit.name
            session.add(categoryToEdit)
            session.commit()
            session.close()
            flash('Category successfully updated.')
            return redirect(url_for('showItems', category_name = editedCategoryName))
    else:
        session.close()
        return render_template('editcategory.html', category = categoryToEdit)


@app.route('/catalog/<category_name>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_name):
    """
    Interface for the admin to delete a category.

    Args:
        item_name (str): Name of the category to be deleted.
    """
    if 'username' not in login_session:
        flash('Please sign in to delete the category.')
        return redirect('/login')
    else:
        if login_session['email'] != app.config['ADMIN_EMAIL']:
            flash('Warning: Only admin(s) can add, remove or modify a category.')
            return redirect(url_for('showCategories'))

    session = db_connect()
    # check for invalid category
    try:
        categoryToDelete = session.query(Category).filter_by(name = category_name).one()
    except NoResultFound:
        flash('Error: Could not find any category named "%s" in the record.' % category_name)
        session.close()
        return redirect(url_for('showCategories'))

    if (request.method == 'POST'):
        session.delete(categoryToDelete)
        flash('Category "%s" successfully deleted !' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        session.close()
        return render_template('deletecategory.html', category = categoryToDelete)


@app.route('/catalog/<category_name>/new', methods=['GET', 'POST'])
def newItem(category_name):
    """
    To add a new item in the catalog.

    Args:
        category_name (str): Name of the category to which item is to be added.
    """
    if 'username' not in login_session:
        flash('Please sign in to add new item')
        return redirect('/login')

    session = db_connect()
    # check for invalid category
    try:
        category = session.query(Category).filter_by(name=category_name).one()
    except NoResultFound:
        flash('Error: Could not find any category named "%s" in the record.' % category_name)
        session.close()
        return redirect(url_for('showCategories'))

    if (request.method == 'POST'):

        # Check for empty name
        if (not request.form['name']) or \
            (request.form['name'].isspace()):
            flash("Error: Item cannot be created with an empty name field.")
            session.close()
            return redirect(url_for('newItem', category_name = category_name))

        # Check for invalid input
        if (request.form['name'].lower() == "categories".lower()) or \
            ((request.form['name'].lower() == "item".lower())) or \
            ((request.form['name'].lower() == "items".lower())):
            # Setting "categories" as category name will cause routing issues
            flash("Error: Route keywords cannot be used as item name(s).")
            session.close()
            return redirect(url_for('newItem', category_name = category_name))

        # Check for duplicate name values
        item = session.query(Item).filter(Item.name == request.form['name'])
        isDuplicate = (session.query(literal(True)).
                          filter(item.exists()).scalar())
        if (isDuplicate):
            flash("Error: Item already exists. "\
                "Please enter a new one.")
            session.close()
            return redirect(url_for('newItem', category_name = category_name))
        else:
            newItem = Item( category_id = category.id,
                            user_id = login_session['user_id'],
                            name = request.form['name'],
                            description = request.form['description'],
                            price = request.form['price'],
                            quantity = request.form['quantity'],)
            session.add(newItem)
            flash('New item "%s" is successfully added.' % newItem.name)
            session.commit()
            session.close()
            return redirect(url_for('showItems', category_name = category_name))
    else:
        session.close()
        return render_template('newitem.html', category = category)


@app.route('/catalog/<category_name>/<item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name, category_name):
    """
    To edit an item in the catalog.

    Args:
        item_name (str): Name of item to be edited.
        category_name (str): Name of the catrgory to which the item belongs.
    """
    if 'username' not in login_session:
        flash('Please sign in to edit your item')
        return redirect('/login')

    session = db_connect()
    # check for invalid category
    try:
        category = session.query(Category).filter_by(name = category_name).one()
        editedItemCategory = category.name
    except NoResultFound:
        flash('Error: Could not find any category named "%s" in the record.' % category_name)
        session.close()
        return redirect(url_for('showCategories'))
    # check for invalid item
    try:
        itemToEdit = session.query(Item).filter_by(name = item_name, category_id = category.id).one()
    except NoResultFound:
        flash('Error: No item named "%s" is in "%s" category.' % (item_name, category_name))
        session.close()
        return redirect(url_for('showItems', category_name = category_name))

    if login_session['user_id'] != itemToEdit.user_id:
        flash("Error: You cannot edit an item that you did not add !")
        return redirect(url_for('showMyItems'))

    if (request.method == 'POST'):
        # Check for empty name
        if (not request.form['name']) or \
            (request.form['name'].isspace()):
            flash("Error: Item cannot be created with an empty name field.")
            session.close()
            return render_template('editItem.html', category = category, item = itemToEdit)
        # Check for invalid input
        if (request.form['name'].lower() == "categories".lower()) or \
            ((request.form['name'].lower() == "item".lower())) or \
            ((request.form['name'].lower() == "items".lower())):
            # Setting "categories" as category name will cause routing issues
            flash("Error: Route keywords cannot be used as item name(s).")
            session.close()
            return render_template('editItem.html', category = category, item = itemToEdit)

        # Check for duplicate name values
        item = session.query(Item).filter(Item.name == request.form['name'])
        isDuplicate = (session.query(literal(True)).
                        filter(item.exists()).scalar())
        if (isDuplicate):
            flash("Error: Item already exists. "\
                "Please enter a new one.")
            session.close()
            return render_template('editItem.html', category = category, item = itemToEdit)
        else:
            itemToEdit.name = request.form['name']
            editedItemName = itemToEdit.name
            if request.form['description']:
                itemToEdit.description = request.form['description']
            if request.form['price']:
                itemToEdit.price = request.form['price']
            if request.form['quantity']:
                itemToEdit.quantity = request.form['quantity']
            session.add(itemToEdit)
            session.commit()
            session.close()
            flash('Item successfully updated.')
            return redirect(url_for('showItem', category_name = editedItemCategory, item_name = editedItemName))
    else:
        session.close()
        return render_template('edititem.html', category = category, item = itemToEdit)


@app.route('/catalog/<category_name>/<item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name, category_name):
    """
    Delete a specified item from the catalog.

    Args:
        item_name (str): Name of the item to be deleted.
        category_name (str): Name of the catrgory to which the item belongs.
    """
    if 'username' not in login_session:
        flash('Please sign in to delete your item')
        return redirect('/login')

    session = db_connect()
    # check for invalid category
    try:
        category = session.query(Category).filter_by(name = category_name).one()
    except NoResultFound:
        flash('Error: Could not find any category named "%s" in the record.' % category_name)
        session.close()
        return redirect(url_for('showCategories'))
    # check for invalid item
    try:
        itemToDelete = session.query(Item).filter_by(name = item_name, category_id = category.id).one()
    except NoResultFound:
        flash('Error: No item named "%s" is in "%s" category.' % (item_name, category_name))
        session.close()
        return redirect(url_for('showItems', category_name = category_name))

    if login_session['user_id'] != itemToDelete.user_id:
        flash("Error: You cannot delete an item that you did not add !")
        return redirect(url_for('showMyItems'))

    if (request.method == 'POST'):
        session.delete(itemToDelete)
        flash('Item "%s" successfully deleted !' % itemToDelete.name)
        session.commit()
        session.close()
        return redirect(url_for('showItems', category_name = category_name))
    else:
        session.close()
        return render_template('deleteitem.html', category = category, item = itemToDelete)