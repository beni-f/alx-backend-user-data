#!/usr/bin/env python3
"""
Auth
"""
import bcrypt
from db import DB
from user import User


def _hash_password(password):
    """
        Hash a password
    """
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, salt=bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email, password):
        """
        Takes email and password as an argument
        then checks if email already exists or
        not and register user accordingly.
        """
        usr_email = self._db._session.query(User).\
            filter_by(email=email).first()
        if usr_email:
            raise ValueError(f'User {email} already exists')
        password = _hash_password(password)
        user = self._db.add_user(email, password)
        return user
