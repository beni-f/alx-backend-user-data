#!/usr/bin/env python3
"""
Auth Class
"""
from typing import List, TypeVar
from flask import request


class Auth():
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            Authentication require path function
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
            Authorization header function
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """
            Figures out the current user
        """
        return None
