from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import asc, desc, literal
from sqlalchemy.orm.exc import NoResultFound

from db_setup import Base, User, Category, Item, DB_URL, db_create
from db_connect import db_connect

app = Flask(__name__)
'''
engine = create_engine(DB_URL+'?check_same_thread=False')
Base.metadata.bind = engine

db_Session = sessionmaker(bind=engine)
session = db_Session()'''

"""
    JSON Endpoints
"""
@app.route('/catalog/JSON')
@app.route('/catalog.json')
def categoryJSON():
    session = db_connect(DB_URL)
    categories = session.query(Category).all()
    return jsonify(Categories = [cat.serialize for cat in categories])


@app.route('/catalog/<category_name>/JSON')
def categoryItemsJSON(category_name):
    session = db_connect(DB_URL)
    category = session.query(Category).filter_by(name = category_name).one()
    #items = session.query(Item).filter_by(category_id = category.id).all()
    return jsonify(category = category.serialize)


@app.route('/catalog/<category_name>/<item_name>/JSON')
def itemJSON(item_name, category_name=None):
    session = db_connect(DB_URL)
    item = session.query(Item).filter_by(name = item_name).one()
    return jsonify(Item = item.serialize)
# End JSON Endpoints


"""
    App Routes
"""
@app.route('/')
@app.route('/catalog/')
def homepage():
    """
    Shows the Homepage that list the 10 recently added items.
    """
    session = db_connect(DB_URL)
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
    session = db_connect(DB_URL)
    categories = session.query(Category).order_by(asc(Category.name)).all()
    if (not categories):
        flash('No category added yet.')
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
    session = db_connect(DB_URL)
    # check for invalid category
    try:
        category = session.query(Category).filter_by(name = category_name).one()
    except NoResultFound:
        flash('No category named "%s" found.' % category_name)
        session.close()
        return redirect(url_for('showCategories'))
    category = session.query(Category).filter_by(name = category_name).one()
    items = session.query(Item).filter_by(category_id = category.id).all()
    if not items:
        flash('No item added yet.')
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
    session = db_connect(DB_URL)
    # check for invalid category
    try:
        category = session.query(Category).filter_by(name = category_name).one()
    except NoResultFound:
        flash('No category named "%s" found.' % category_name)
        session.close()
        return redirect(url_for('showCategories'))
    # check for invalid item
    try:
        item = session.query(Item).filter_by(name = item_name, category_id = category.id).one()
    except NoResultFound:
        flash('No item named "%s" found in "%s" category.' % (item_name, category_name))
        session.close()
        return redirect(url_for('showItems', category_name = category_name))
    #category = session.query(Category).filter_by(name = category_name).one()
    #item = session.query(Item).filter_by(name = item_name).one()
    session.close()
    return render_template('item.html', item = item, category = category)


@app.route('/catalog/myitems/')
def showMyItems():
    """
    Displays the items added by a user.
    """
    return 'Shows the items added by a users.'


@app.route('/catalog/new', methods=['GET', 'POST'])
def newCategory():
    """
    Interface for the admin to add a new category.
    """
    if request.method == 'POST':
        session = db_connect(DB_URL)

        # Check for empty name
        if (not request.form['name']) or \
            (request.form['name'].isspace()):
            flash("Cannot add a category without a name.")
            session.close()
            return redirect(url_for('newCategory'))

        # Check for invalid input
        if (request.form['name'].lower() == "categories".lower()):
            # Setting "categories" as category name will cause routing issues
            flash("You cannot use that word as a category's name.")
            session.close()
            return redirect(url_for('newCategory'))

        # Check for duplicate category name
        category = session.query(Category).filter(Category.name == request.form['name'])
        isDuplicate = (session.query(literal(True)).
                          filter(category.exists()).scalar())
        if (isDuplicate):
            flash("Name already exists. "\
                "Please enter a new name.")
            session.close()
            return redirect(url_for('newCategory'))
        else:
            newCategory = Category(name = request.form['name'])
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
    Interface for the admin to edit a category.

    Args:
    category_name (str): Name of category to be edited.
    """
    session = db_connect(DB_URL)
    # check for invalid category
    try:
        categoryToEdit = session.query(Category).filter_by(name = category_name).one()
    except NoResultFound:
        flash('No category named "%s" found.' % category_name)
        session.close()
        return redirect(url_for('showCategories'))

    if (request.method == 'POST'):
        # Check for empty name
        if (not request.form['name']) or \
            (request.form['name'].isspace()):
            flash("You cannot set the name empty.")
            session.close()
            return render_template('editcategory.html', category = categoryToEdit)

        # Check for invalid input
        if (request.form['name'].lower() == "categories".lower()):
            # Setting "categories" as category name will cause routing issues
            flash("You cannot use that word as a category name.")
            session.close()
            return render_template('editcategory.html', category = categoryToEdit)

        # Check for self duplicate -- not much needed though
        if (request.form['name'] == categoryToEdit.name):
            flash("Please modify the name to some new value.")
            session.close()
            return render_template('editcategory.html', category = categoryToEdit)

        # Check for duplicate with category name
        category = session.query(Category).filter(Category.name == request.form['name'])
        isDuplicate = (session.query(literal(True)).
                          filter(category.exists()).scalar())
        if (isDuplicate):
            flash("Category name already exists. "\
                "Please enter a new name.")
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
    session = db_connect(DB_URL)
    # check for invalid category
    try:
        categoryToDelete = session.query(Category).filter_by(name = category_name).one()
    except NoResultFound:
        flash('No category named "%s" found.' % category_name)
        session.close()
        return redirect(url_for('showCategories'))

    if (request.method == 'POST'):
        session.delete(categoryToDelete)
        flash('Category "%s" successfully deleted' % categoryToDelete.name)
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
    session = db_connect(DB_URL)
    # check for invalid category
    try:
        category = session.query(Category).filter_by(name=category_name).one()
    except NoResultFound:
        flash('No category named "%s" found.' % category_name)
        session.close()
        return redirect(url_for('showCategories'))

    if (request.method == 'POST'):

        # Check for empty name
        if (not request.form['name']) or \
            (request.form['name'].isspace()):
            flash("Cannot add an item without a name.")
            session.close()
            return redirect(url_for('newItem', category_name = category_name))

        # Check for invalid input
        if (request.form['name'].lower() == "categories".lower()) or \
            ((request.form['name'].lower() == "item".lower())) or \
            ((request.form['name'].lower() == "items".lower())):
            # Setting "categories" as category name will cause routing issues
            flash("You cannot use that word as a category's name.")
            session.close()
            return redirect(url_for('newItem', category_name = category_name))

        # Check for duplicate name values
        item = session.query(Item).filter(Item.name == request.form['name'])
        isDuplicate = (session.query(literal(True)).
                          filter(item.exists()).scalar())
        if (isDuplicate):
            flash("Item name already exists. "\
                "Please enter a new name.")
            session.close()
            return redirect(url_for('newItem', category_name = category_name))
        else:
            newItem = Item( category_id = category.id,
                            user_id = 1, # need to be updated
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
    session = db_connect(DB_URL)
    # check for invalid category
    try:
        category = session.query(Category).filter_by(name = category_name).one()
        editedItemCategory = category.name
    except NoResultFound:
        flash('No category named "%s" found.' % category_name)
        session.close()
        return redirect(url_for('showCategories'))
    # check for invalid item
    try:
        itemToEdit = session.query(Item).filter_by(name = item_name, category_id = category.id).one()
    except NoResultFound:
        flash('No item named "%s" found in "%s" category.' % (item_name, category_name))
        session.close()
        return redirect(url_for('showItems', category_name = category_name))

    if (request.method == 'POST'):
        # Check for empty name
        if (not request.form['name']) or \
            (request.form['name'].isspace()):
            flash("You cannot set the name empty.")
            session.close()
            return render_template('editItem.html', category = category, item = itemToEdit)
        # Check for invalid input
        if (request.form['name'].lower() == "categories".lower()) or \
            ((request.form['name'].lower() == "item".lower())) or \
            ((request.form['name'].lower() == "items".lower())):
            # Setting "categories" as category name will cause routing issues
            flash("You cannot use that word as a category's name.")
            session.close()
            return render_template('editItem.html', category = category, item = itemToEdit)

        # Check for duplicate name values
        item = session.query(Item).filter(Item.name == request.form['name'])
        isDuplicate = (session.query(literal(True)).
                        filter(item.exists()).scalar())
        if (isDuplicate):
            flash("Item name already exists. "\
                "Please enter a new name.")
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
    session = db_connect(DB_URL)
    # check for invalid category
    try:
        category = session.query(Category).filter_by(name = category_name).one()
    except NoResultFound:
        flash('No category named "%s" found.' % category_name)
        session.close()
        return redirect(url_for('showCategories'))
    # check for invalid item
    try:
        itemToDelete = session.query(Item).filter_by(name = item_name, category_id = category.id).one()
    except NoResultFound:
        flash('No item named "%s" found in "%s" category.' % (item_name, category_name))
        session.close()
        return redirect(url_for('showItems', category_name = category_name))

    if (request.method == 'POST'):
        session.delete(itemToDelete)
        flash('Item "%s" successfully deleted' % itemToDelete.name)
        session.commit()
        session.close()
        return redirect(url_for('showItems', category_name = category_name))
    else:
        session.close()
        return render_template('deleteitem.html', category = category, item = itemToDelete)


if __name__ == '__main__':
    # secret key needs to be changed in production env
    app.secret_key ='super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)