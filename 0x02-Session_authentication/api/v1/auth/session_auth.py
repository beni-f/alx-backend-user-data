#!/usr/bin/env python3
"""
Session Auth
"""
from .auth import Auth
import uuid


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
        key = uuid.uuid4()
        self.user_id_by_session_id[key] = user_id
        return key
