#!/usr/bin/env python3
"""
Basic Auth
"""
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
        Basic Authentication
    """
    def extract_base64_authorization_header(self, authorization_header: str) \
            -> str:
        """
            Returns the Base64 part of the
            Authorization header for a Basic Authentication
        """
        if not authorization_header or\
                not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[-1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """
            Returns the decoded value of a Base64 string
        """
        if not base64_authorization_header or\
                not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_authorization_header = \
                base64.b64decode(base64_authorization_header)
            return decoded_authorization_header.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):  # type: ignore
        """
            Returns the user email and password from the Base64 decoded value
        """
        if not decoded_base64_authorization_header or\
                not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_info = decoded_base64_authorization_header.split(':', 1)
        print(user_info)
        return user_info[0], user_info[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):  # type: ignore
        """
            Returns the User instance based on his email and password
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return users[0]

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """
            Retrives the User instance for a request
        """
        authorization_header = \
            self.extract_base64_authorization_header(
                request.headers['Authorization']
            )
        decoded_info = \
            self.decode_base64_authorization_header(authorization_header)
        user_email, user_pwd = self.extract_user_credentials(decoded_info)
        return self.user_object_from_credentials(user_email, user_pwd)
