#!/usr/bin/env python3
"""
    The below module defines the Auth class,
    which provides basic authentication
    and authorization mechanisms
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """
    Auth class provides methods for auth
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Decidess if the requested path requires authentication.

        Args:
            path (str): The requested path.
            excluded_paths (List[str]): A list of paths
        Returns:
            bool: True if the path requires authentication,
            False otherwise.
        """
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True
        if path[-1] != '/':
            path += '/'
        for ex_path in excluded_paths:
            if ex_path.endswith('*'):
                if path.startswith(ex_path[:1]):
                    return False
        return False if path in excluded_paths else True

    def authorization_header(self, request=None) -> str:
        """Auth that returns True if the path is not in
        the list of strings excluded_paths """
        if request:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ main point of entry """
        return None
