#!/usr/bin/env python3
"""
Below is a class to manage the API auth.
in the folder api/v1/auth we shall
have auth.py below
"""


from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Class for handling API auth nd authorization """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        if the given endpoint requires authentication.
        Returns:
            bool: True if authentication is required
            False otherwise.
        """
        if not path or not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'
        for ex_path in excluded_paths:
            if path[:ex_path.find('*')] in ex_path[:ex_path.find('*')]:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        below retrieves the Authorization header from the request.
        returns None - request will be the Flask request object
        Returns:
            str(string): The Authorization header if present
            None if otherwise.
        """
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request.
        returns None - request will be the Flask request object
        Returns:
            User: The current user if present
            None if otherwise
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns: a cookie value from a request
        the value of the cookie named _my_session_id from request
        """
        if request:
            return request.cookies.get(getenv('SESSION_NAME'))
