#!/usr/bin/env python3
"""
Below is a module for handling Basic Authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar
class BasicAuth(Auth):
    """
    below is a class for Basic authentication from the auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic Authentication
        Returns:
                str: The Base64 part of the authorization header or None.
        """
        if authorization_header is None or type(authorization_header) != str:
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ Decodes the Base64 part of the Authorization header

        Arguments:
            base64_auth_header (str): The Base64 part
        Retrns: str: The decoded string or None.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded64 = b64decode(encoded)
            decoded = decoded64.decode('utf-8')
        except BaseException:
            return None

        return decoded

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Extracts user credentials from the decoded Base64 authorization header

        Args:
            decoded_base64_auth_header (str): The decoded Base64
        Returns: tuple containing: email, passwd or none none
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        credentials = decoded_base64_authorization_header.split(':', 1)

        return credentials[0], credentials[1]

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
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            found_users = User.search({'email': user_email})
        except Exception:
            return None

        for user in found_users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on
        the Authorization header in the request
        Arguments:
            request(Flask): The req obj. Defaults to None.
        Returns:
            User: The current usr obj if authorization is valid
            false if otherwise
        """
        authntctd_header = self.authorization_header(request)

        if not authntctd_header:
            return None

        encoded = self.extract_base64_authorization_header(authntctd_header)

        if not encoded:
            return None

        decoded = self.decode_base64_authorization_header(encoded)

        if not decoded:
            return None

        email, pwd = self.extract_user_credentials(decoded)

        if not email or not pwd:
            return None
        user = self.user_object_from_credentials(email, pwd)

        return user