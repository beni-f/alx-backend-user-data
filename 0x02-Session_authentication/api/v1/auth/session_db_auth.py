#!/usr/bin/env python3
"""
Session ID based database storage
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
       Session Database Authentication
    """
    def create_session(self, user_id: str = None) -> str:
        """
            Creates and stores new instance of
            UserSession and returns the session ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
            Returns the User ID by requesting
            UserSession in the database based on session_id
        """
        if not session_id:
            return None
        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return None
        session = sessions[0]
        if self.session_duration <= 0:
            return session.user_id
        created_at = session.created_at
        if created_at is None:
            return None
        if created_at + timedelta(seconds=self.session_duration)\
                < datetime.now():
            return None
        return session.user_id

    def destory_session(self, request=None) -> bool:
        """
            Destroy the UserSession based on the Session ID
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False
        session = session[0]
        session.remove()
        return True
