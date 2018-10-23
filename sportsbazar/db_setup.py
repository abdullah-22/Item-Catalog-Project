"""
    Database setup for the Item Catalog project.
    This script should be run before running the main application.py file
    and then the db_populate.py file to fill the databse with the test data.
    The database is contain following tables and attributes:
    -- user: id, name, email, picture
    -- category: id, name, user_id
    -- item: id, name, description, price, quantity, category_id, user_id
"""


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


DB_URL = "sqlite:///sportsbazar.db?check_same_thread=False"


# Base class mapper from SQLalchemy
Base = declarative_base()


class User(Base):
    """
        Table to store users' information.

        Attributes:
            __tablename__: Name of the table.
            id: User ID of the resgistered user.
            name: Name of the user.
            email: Email of the user.
            picture: URL of the user's picture.
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    """
        Table to store categories / item type information.

        Attributes:
            __tablename__: Name of the table.
            id: ID for each category of items.
            name: Name of the category.
            user_id: ID of the user / owner.
            user: Relationship with the user / owner.
            items: Relationship with individual items.
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    items = relationship('Item', cascade="save-update, merge, delete")

    # To return category data in aa serialiseable format for JSON API.
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'Items': [i.serialize for i in self.items]
        }


class Item(Base):
    """
        Define table for items / SKUs.

        Attributes:
            __tablename__: Name of the table.
            id: ID for each item.
            name: Name of item.
            description: Description of the item.
            price: Price of single unit.
            quantity: Quantity of items in inventory.
            category_id: ID of the category that the item belongs to.
            category: Relationship with the category / item type.
            user_id: User ID of the owner of the item.
            user: Relationship with the user (owner / vendor) of the item.
    """
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # To return category data in aa serialiseable format for the JSON API.
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity,
            'category_id': self.category_id
        }


def db_create(DB_URL):
    """
        Creates a new empty database.

        Args:
            db_url: Path for new db file
    """
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    print "Database created successfully ..."


if __name__ == '__main__':
    db_create(DB_URL)