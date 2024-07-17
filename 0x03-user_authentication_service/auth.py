#!/usr/bin/env python3
"""
Auth
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
        Hash a password
    """
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, salt=bcrypt.gensalt())


def _generate_uuid() -> str:
    """
        Return a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initialization
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Takes email and password as an argument
        then checks if email already exists or
        not and register user accordingly.
        """
        try:
            usr_email = self._db.find_user_by(email=email)
            if usr_email:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            password = _hash_password(password)
            user = self._db.add_user(email, password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Checks if login details are valid or not
        """
        try:
            usr = self._db.find_user_by(email=email)
            if usr:
                return bcrypt.checkpw(
                    password.encode('utf-8'), usr.hashed_password
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
            Creates a session id for the user.
        """
        try:
            usr = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(usr.id, session_id=session_id)
        return session_id
