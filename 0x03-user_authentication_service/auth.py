#!/usr/bin/env python3
"""
Auth
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
        Hash a password
    """
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, salt=bcrypt.gensalt())


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
