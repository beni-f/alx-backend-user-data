#!/usr/bin/env python3
"""
Auth Class
"""
from typing import List, TypeVar
from flask import request


class Auth():
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            Not used yet.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
            Not used yet.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """
            Not used yet.
        """
        return None
