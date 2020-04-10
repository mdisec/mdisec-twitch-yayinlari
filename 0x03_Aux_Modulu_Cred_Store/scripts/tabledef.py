# -*- coding: utf-8 -*-

import sys
import os
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Local
SQLALCHEMY_DATABASE_URI = 'postgresql://twitch:twitch@localhost:5432/twitch'

# Heroku
#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(SQLALCHEMY_DATABASE_URI)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    password = Column(String(512))
    email = Column(String(50))

    def __repr__(self):
        return '<User %r>' % self.username


class LogModel(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    ip = Column(String())
    user_agent = Column(String())

    def __init__(self, ip, user_agent):
        self.ip = ip
        self.user_agent = user_agent

    def __repr__(self):
        return f"<Log {self.ip}>"



engine = db_connect()  # Connect to database
Base.metadata.create_all(engine)  # Create models
