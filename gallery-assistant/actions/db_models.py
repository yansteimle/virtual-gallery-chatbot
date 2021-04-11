# db_models.py
# We use SQLAlchemy with an SQLite database.
# This file contains the declarative base and the classes for the persistent data
# we want to save in the sqlite database
# Resources consulted:
# https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
# https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
# https://realpython.com/python-sqlite-sqlalchemy/
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#association-object
# https://docs.sqlalchemy.org/en/14/core/engines.html
#############################################
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Enum

# Set echo=True to get the SQL queries made printed out on the standard output
# engine = create_engine('sqlite:///gallery.db', echo=False)  # sqlalchemy engine that will interact with sqlite db
# Absolute path to gallery database (since we call create_engine() function from two directories, need an absolute path)
db_path = '/Users/yansteimle/Projects/gallery-assistant/gallery.db'  # change depending on file system
engine = create_engine(f'sqlite:///{db_path}', echo=False)
Session = sessionmaker(bind=engine)  # session factory bound to the engine

Base = declarative_base()  # base class for class definitions


class Bid(Base):
    """Association object class that provides an association table between the
    user and artwork tables with additional information (i.e. the value of the bid)."""
    __tablename__ = 'bid'
    user_name = Column(Integer, ForeignKey('user.user_name'), primary_key=True)
    artwork_id = Column(String, ForeignKey('artwork.artwork_id'), primary_key=True)
    value = Column(Integer)  # value of the bid
    user = relationship("User", back_populates="bids")
    artwork = relationship("Artwork", back_populates="bidders")


class User(Base):
    """Class for the users (i.e. the clients). Only contains user_name
    (for a real web application, there would be extra information such as email,
    hashed password, etc.)."""
    __tablename__ = 'user'
    user_name = Column(String(20), primary_key=True)  # must be unique as it is used as primary key
    bids = relationship("Bid", back_populates='user')


class Artwork(Base):
    """Class for the artwork. Note that for a real web application, there would be another
    table for artists with information about each artists and a many-to-one relation
    from artwork to artist. However, for this simplified example, we just save the artist name
    directly in the artwork table."""
    __tablename__ = 'artwork'
    artwork_id = Column(String(6), primary_key=True)  # format: ABC123, must be unique
    title = Column(String(50))
    artist_name = Column(String(30))
    medium = Column(String(50))
    category = Column(String(20))  # 'drawing', 'painting', 'sculpture', 'photography', 'other'
    min_bid = Column(Integer)  # minimum bid amount
    bidders = relationship("Bid", back_populates='artwork')
