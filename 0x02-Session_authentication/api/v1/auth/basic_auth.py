#!/usr/bin/env python3
"""
BasicAuth class to manage API authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """
    below is a class for Basic authentication from the auth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for Basic Authentication
        Returns:
            str: The Base64 part of the authorization header or None.
        """
        if (isinstance(authorization_header, str) and
                authorization_header.startswith('Basic ')):
            return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
         Decodes the Base64 part of the Authorization header

        Arguments:
            base64_auth_header (str): The Base64 part
        Retrns: str: The decoded string or None.
        """
        try:
            return base64.b64decode(
                base64_authorization_header.encode('utf-8')).decode('utf-8')
        except Exception:
            return

    def extract_user_credentials(self, dcode: str) -> (str, str):
        """
        Extracts user credentials from the decoded Base64 authorization header

        Args:
            decoded_base64_auth_header (str): The decoded Base64
        Returns: tuple containing: email, passwd or none none
        """
        if (not isinstance(dcode, str) or ':' not in dcode):
            return (None, None)
        return (dcode[:dcode.find(':')], dcode[dcode.find(':') + 1:])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
                Retrieves the usr obj based on email and password
        Arguments:
            user_email (str): The user's email.
            user_password (str): The user's password.
        Returns:
                none, none
        """
        if (user_email and user_pwd and isinstance(user_email, str) and
                isinstance(user_pwd, str)):
            try:
                users = User.search({'email': user_email})
            except Exception:
                return
            for usr in users:
                if usr.is_valid_password(user_pwd):
                    return usr

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user based on
        the Authorization header in the request
        Arguments:
            request(Flask): The req obj. Defaults to None.
        Returns:
            User: The current usr obj if authorization is valid
            false if otherwise
        """
        header = self.authorization_header(request)
        b64 = self.extract_base64_authorization_header(header)
        decode = self.decode_base64_authorization_header(b64)
        user, pwd = self.extract_user_credentials(decode)
        return self.user_object_from_credentials(user, pwd)
