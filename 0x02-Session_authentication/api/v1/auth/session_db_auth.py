#!/usr/bin/env python3
"""
The beow module defines the SessionDBAuth class
SessionExpAuth class
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    Session DB authentication class
    session management with database persistence
    """

    def create_session(self, user_id=None):
        """
        Creates a session for a user and saves it to the database.

        Args:
            user_id (str): The ID of the user
        Returns(str):
            The session ID if a session was created
        """
        if user_id:
            session_id = super().create_session(user_id)
            usrsess = UserSession(user_id=user_id, session_id=session_id)
            usrsess.save()
            UserSession.save_to_file()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with a given session ID.

        Args:
            session_id (str): The session ID
        """
        if not session_id:
            return None
        UserSession.load_from_file()
        users = UserSession.search({'session_id': session_id})
        for usr in users:
            sessexp = timedelta(seconds=self.session_duration)
            if usr.created_at + sessexp < datetime.now():
                return None
            return usr.user_id

    def destroy_session(self, request=None):
        """
        Destroys a session associated with the request.
        Returns(bool):
            True if the session was successfully destroyed
        """
        if request:
            session_id = self.session_cookie(request)
            if not session_id:
                return False
            if not self.user_id_for_session_id(session_id):
                return False
            user_sess = UserSession.search({'session_id': session_id})
            for usr in user_sess:
                usr.remove()
                UserSession.save_to_file()
                return True
        return False
