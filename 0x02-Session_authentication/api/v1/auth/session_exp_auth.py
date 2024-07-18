#!/usr/bin/env python3
"""
the below module defines the SessionExpAuth class
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class provides session management
    handles expiration.
    """

    def __init__(self):
        """
        Initialize the SessionExpAuth instance
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a new session for the given user ID
        includes the formation of a time stamp
        Argumentss:
            user_id (str): The ID of the user
        Returns(str):
            The session ID if a session was created
        """
        session_id = super().create_session(user_id)
        if session_id:
            SessionAuth.user_id_by_session_id[session_id] = {
                'user_id': user_id, 'created_at': datetime.now()}
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID associated with a given session ID
        Arguments:
            session_id (str): The session ID to search for
        """
        if not session_id:
            return None
        sess_data = SessionExpAuth.user_id_by_session_id.get(session_id)
        if not sess_data:
            return None
        if self.session_duration <= 0:
            return sess_data['user_id']
        if 'created_at' not in sess_data:
            return None
        sess_exp = timedelta(seconds=self.session_duration)
        if sess_data['created_at'] + sess_exp < datetime.now():
            return None
        return sess_data['user_id']
