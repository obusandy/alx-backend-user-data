#!/usr/bin/env python3
"""
module defines the User class using SQLAlchemy for ORM
using the mapping declaration of SQLAlchemy
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class User(Base):
    """
    User class rep a usr entity in the db
    Attr:
    id: int primary key
        The database tablename is rep by
        the str __tablename__.
        The user table's primary key is user_id (int).
        User's email address (user_email (str)).
        user_hashed_password (str):
            The user's hashed password.
        user_session_id (str):
            The user's session ID.
        ser_reset_token (str):
            The reset token for passwd recovery.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
