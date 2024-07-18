#!/usr/bin/env python3
"""
dbse module
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
from user import Base, User


DATA = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    """DB class that implements add user method"""
    def __init__(self):
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        below is used to add user to the db
        Args:
            user_email (str): The email of the user.
            user_hashed_password (str):
                The hashed password of the user.
        """
        if not email or not hashed_password:
            return
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user in the database
        returns the first row found in the users
        table as filtered by the methods input arguments
        Args:
            **search_params:
            Arbitrary keyword args for search criteria
        Returns:
            User: The user object that matches the search criteria
        Raises:
            NoResultFound: If no user matches the search
        """
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's information in the database.
        Args:
            user_id (int): The ID of the user to update.
            **update_fields:
            Arbitrary keyword args for fields to update.
        Raises:
            ValueError: If any of the fields to update are not allowed

        """
        user = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if key not in DATA:
                raise ValueError
            setattr(user, key, val)
        self._session.commit()
        return None
