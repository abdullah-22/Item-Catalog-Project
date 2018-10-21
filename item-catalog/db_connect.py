"""
    Methods to handle connection with the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base

def db_connect(DB_URL):
    """
        Connects to the database and returns an sqlalchemy session object.
    """
    engine = create_engine(DB_URL)
    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    session = db_session()

    return session