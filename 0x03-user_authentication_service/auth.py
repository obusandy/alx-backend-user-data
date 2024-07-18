#!/usr/bin/env python3
"""
below is a Authentication module to handle
-user registration, login, session management,
and password reset functionalities
using SQLAlchemy and bcrypt for hashing.
"""
from db import DB
from uuid import uuid4
from user import User
from bcrypt import hashpw, gensalt, checkpw
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """
    define a _hash_password method that
    takes in a password string arguments
    returns: bytes.
    salted hash of the input password,
    hashed with bcrypt.hashpw.
    """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """
    Generate a new UUID.

    Returns: A new UUID string.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the
    authentication databse.
    """

    def __init__(self):
        """Initialize the Auth class with a db connection"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the given email and password.

        Argumentss:
            email (str): The email of the new usr.
            password (str):
            The plain txt passwd of the newusr.

        Returns:
            User:
            The newly created user obj.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """
        expect email and password required args
        returns: a boolean.
        check the password with bcrypt.checkpw.
        If it matches return True.
        otherwise, return False
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return checkpw(password.encode('utf-8'), user.hash_password)

    def create_session(self, email: str) -> str:
        """
        Creates a user session
        Returns:
            str: The session ID for the new session.
        args: email
            email of the user
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
        except NoResultFound:
            return

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        Get the email of the user associated with the given session ID.
        Arguments:
            session_id (str): The session ID.
        Returns:
            string: which is the email of the user
        """
        if session_id is None:
            return
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user.email
        except NoResultFound:
            return

    def destroy_session(self, user_id: int) -> None:
        """
        destroys the associated token
        Args: user_id
            The ID of the user.
        returns none
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a passwd reset token for the usr
        with the given email.
        Args:
            email (str): The email of the user.
        Returns:
            str: The passwd reset token.
        Raises:
            ValueError: If no user with the given email exists.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update the passwd for the user.

        Args:
            reset_token (str):
                The password reset token.
            password (str):
                The new plain text passwd.
        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
