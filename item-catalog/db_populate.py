"""
    Script to fill the databse with test data.

    This application is to be an online catalog where different users
    can resgister and list items in different categories.

    Initially, an inventory of clothing
    and accessories is used as the test data.

    This script is to run for the first time
    only after the fresh creation of the database.
"""

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User, Category, Item, DB_URL
from db_connect import db_connect


def db_populate():
    """
        Fills the database with the test data.
    """

    session = db_connect(DB_URL)

    # Makes sure the database is empty else return.
    category_count = session.query(func.count(Category.id)).scalar()
    if category_count > 0:
        session.close()
        return

    # Creates categories of items.
    category1 = Category(name="Cricket")
    session.add(category1)
    session.commit()

    category2 = Category(name="Football")
    session.add(category2)
    session.commit()

    category3 = Category(name="Hockey")
    session.add(category3)
    session.commit()

    category4 = Category(name="Basket Ball")
    session.add(category4)
    session.commit()

    category5 = Category(name="Snooker")
    session.add(category5)
    session.commit()

    # Adds dummy user for these initial items
    user1 = User(name="Admin", email="admin@domain.com")
    session.add(user1)
    session.commit()

    # Adds items -- Cricket
    item1 = Item(
        user=user1,
        category=category1,
        name="Bat",
        description=(
            "Made with imported English Willow - Super Sixer Series."
        ),
        price=80,
        quantity=100,
    )
    session.add(item1)
    session.commit()

    item2 = Item(
        user=user1,
        category=category1,
        name="Kits",
        description=(
            "100 percent cotton - white color - full sleeves"
        ),
        price=40,
        quantity=50,
    )
    session.add(item2)
    session.commit()

    # Adds items -- Football
    item3 = Item(
        user=user1,
        category=category2,
        name="Shoes",
        description=(
            "Original Addidas Predator - All sizes available"
        ),
        price=200,
        quantity=100,
    )
    session.add(item3)
    session.commit()

    item4 = Item(
        user=user1,
        category=category2,
        name="Football",
        description=(
            "A-Copy of Telstar-18 - Official Ball of FIFA 2018"
        ),
        price=200,
        quantity=50,
    )
    session.add(item4)
    session.commit()

    # Adds items -- Hockey
    item5 = Item(
        user=user1,
        category=category3,
        name="Stick",
        description=(
            "Swagger Pro 2018 - with full flexible cane handle"
        ),
        price=50,
        quantity=50,
    )
    session.add(item5)
    session.commit()

    item6 = Item(
        user=user1,
        category=category3,
        name="Helmet",
        description=(
            "Carbon fibre super strong - Noster1"
        ),
        price=100,
        quantity=30,
    )
    session.add(item6)
    session.commit()

    # Add items -- BasketBall
    item7 = Item(
        user=user1,
        category=category4,
        name="Shirts",
        description=(
            "New designs 2018"
        ),
        price=15,
        quantity=100,
    )
    session.add(item7)
    session.commit()

    item8 = Item(
        user=user1,
        category=category4,
        name="Socks",
        description=(
            "Super bowl printed nylon flexible socks"
        ),
        price=8,
        quantity=30,
    )
    session.add(item8)
    session.commit()

    # Add items -- Snooker
    item9 = Item(
        user=user1,
        category=category5,
        name="Cue Stick",
        description=(
            "3 pieces shock absorbing willow sticks"
        ),
        price=150,
        quantity=10,
    )
    session.add(item9)
    session.commit()

    item10 = Item(
        user=user1,
        category=category5,
        name="Kit",
        description=(
            "Exclusive cue case with chalk holder and chalk"
        ),
        price=170,
        quantity=5,
    )
    session.add(item10)
    session.commit()

    session.close()
    print "Test data populated ..."


if __name__ == '__main__':
    db_populate()
