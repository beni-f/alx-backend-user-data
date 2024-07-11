#!/usr/bin/env python3
"""
Session Auth
"""
from typing import TypeVar

from flask.json import jsonify
from .auth import Auth
import uuid
import os
from flask import request
from models.user import User
from api.v1.views import app_views


class SessionAuth(Auth):
    """"
        Session Authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
            Generates a session id for a user given by user_id
        """
        if not user_id or not isinstance(user_id, str):
            return None
        key = str(uuid.uuid4())
        self.user_id_by_session_id[key] = user_id
        return key

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
            Retrieves user's id from the session id given
        """
        if not session_id:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """
            Retrieves a User instance from the database.
        """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user

    def destory_session(self, request=None):
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        if not self.user_id_for_session_id(session_id):
            return False
        del self.user_id_by_session_id[session_id]
        return True
