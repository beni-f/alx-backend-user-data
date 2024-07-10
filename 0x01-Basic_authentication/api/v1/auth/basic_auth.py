#!/usr/bin/env python3
"""
Basic Auth
"""
from .auth import Auth
import base64


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
        if not decoded_base64_authorization_header or\
              not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_info = decoded_base64_authorization_header.split(':')
        return user_info[0], user_info[1]
