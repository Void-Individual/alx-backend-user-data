#!/usr/bin/env python3
"""Module for authentication"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Takes a mandatory email and pwd and returns a user object"""

        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pwd = _hash_password(password)
            user = self._db.add_user(email, pwd)
            return user


def _hash_password(Password: str) -> bytes:
    """Method to take in a str password and return bytes"""

    encode = Password.encode('utf-8')
    hashed = bcrypt.hashpw(encode, bcrypt.gensalt())

    return hashed
