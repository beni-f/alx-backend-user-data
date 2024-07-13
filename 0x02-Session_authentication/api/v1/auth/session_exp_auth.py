#!/usr/bin/env python3
"""
session_exp_auth
"""
from .session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    Adds an expiration date to a Session ID
    """
    def __init__(self):
        """
            Initialization
        """
        super().__init__()
        self.session_duration = int(os.getenv('SESSION_DURATION', '0'))

    def create_session(self, user_id: str = None) -> str:
        """
            Create a session ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
            Returns user id from a given session id
        """
        if not session_id:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        if not created_at:
            return None
        if created_at + timedelta(seconds=self.session_duration)\
                < datetime.now():
            return None
        return session_dict.get('user_id')
