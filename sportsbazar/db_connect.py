"""
    Methods to handle connection with the database.
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sportsbazar import app
from sportsbazar.db_setup import Base, DB_URL


def db_connect():
    """
        Connects to the database and returns an sqlalchemy session object.
    """
    engine = create_engine(DB_URL)
    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    session = db_session()

    return session
