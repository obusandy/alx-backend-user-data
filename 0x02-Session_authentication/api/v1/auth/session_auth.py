#!/usr/bin/env python3
""" Module for Session Authentication """


from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth (Auth):
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
        if isinstance(user_id, str):
            session_id = str(uuid.uuid4())
            SessionAuth.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """below is an instance method that
            Returns: a User ID based on a Session ID:
            Returns: None if session_id is None
            Returns: None if session_id is not a string
        """
        if isinstance(session_id, str):
            return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        an instance method (overload) that
        returns a User instance based on a cookie value
        Attr:
            self
        """
        return User.get(
            self.user_id_for_session_id(self.session_cookie(request)))

    def destroy_session(self, request=None):
        """
        cla destroy session that deletes the user session / logout:

        Args:
            request: The request object containing the session cookie.
        Returns: FalseIf the request is equal to None
        Returns: FalseIf the request doesnt contain the Session ID cookie
        """

        if request:
            session_id = self.session_cookie(request)
            if not session_id:
                return False
            if not self.user_id_for_session_id(session_id):
                return False
            self.user_id_by_session_id.pop(session_id)
            return True
