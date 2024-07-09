#!/usr/bin/env python3
"""
Auth Class
"""
from typing import List, TypeVar
from flask import request


class Auth():
    """
        Auth Class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            Checks if the path given is in the excluded_paths list

            if path is in excluded_paths list, returns False

            if path is None, returns True

            if excluded_paths is None or empty, returns True
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        else:
            for p in excluded_paths:
                if p[-1] == '/' and path[-1] == '/':
                    p = p[:-1]
                    path = path[:-1]
                if p[-1] == '/':
                    p = p[:-1]
                if p == path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
            Authorization header function
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """
            Figures out the current user
        """
