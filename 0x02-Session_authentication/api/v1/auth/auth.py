#!/usr/bin/env python3
"""Below is a class to manage the API authentication.
in the folder api/v1/auth we shall have auth.py below
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Class for handling API auth nd authorization
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        if the given endpoint requires authentication.
        Returns:
            bool: True if authentication is required
            False otherwise.
        """
        if path is None or excluded_paths is None:
            return True
        nd_point = len(path)
        if nd_point == 0:
            return True

        slash_trailpath = True if path[nd_point - 1] == '/' else False

        tmprraypath = path
        if not slash_trailpath:
            tmprraypath += '/'

        for pubndpint in excluded_paths:
            ttl_ndpoint = len(pubndpint)
            if ttl_ndpoint == 0:
                continue

            if pubndpint[ttl_ndpoint - 1] != '*':
                if tmprraypath == pubndpint:
                    return False
            else:
                if pubndpint[:-1] == path[:ttl_ndpoint - 1]:
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
        if request is None:
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
        if request is None:
            return None

        session_name = getenv('SESSION_NAME')

        if session_name is None:
            return None

        return request.cookie.get(session_name)