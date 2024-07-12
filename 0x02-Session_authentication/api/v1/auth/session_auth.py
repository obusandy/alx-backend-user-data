#!/usr/bin/env python3
""""""
from models.user import User
from .auth import Auth
from uuid import uuid4

class SessionAuth(Auth):
    """
    a class SessionAuth that inherits from Auth.
    this class is empty.
    first step for creating a new authentication mechanism
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        a class attr user_id_by_session_id initialized by an empty dict
        creates a Session ID for a user_id:
            Returns: None if user_id is None
            Returns: None if user_id is not a string
        """
        if user_id and isinstance(user_id, str):
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """below is an instance method that
        Returns: a User ID based on a Session ID:
        Returns: None if session_id is None
        Returns: None if session_id is not a string
        """
        if session_id and isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id, None)
        return None

    def current_user(self, request=None):
        """
        an instance method (overload) that
        returns a User instance based on a cookie value
        Attr:
            self
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        cla destroy session that deletes the user session / logout:

        Args:
            request: The request object containing the session cookie.
        Returns: FalseIf the request is equal to None
        Returns: FalseIf the request doesnt contain the Session ID cookie
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
