#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt
from typing import ByteString


def hash_password(password: str) -> ByteString:
    """
        returns a salted, hashed password
    """
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())
