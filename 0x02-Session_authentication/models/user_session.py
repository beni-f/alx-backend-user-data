#!/usr/bin/env python3
"""
Database for User Session
"""
from .base import Base


class UserSession(Base):
    """
        Database to store Session ID besides other user information
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
            Initialization
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
