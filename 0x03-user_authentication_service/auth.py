#!/usr/bin/env python3
"""Module for authentication"""

import bcrypt
import uuid
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

    def valid_login(self, email: str, password: str) -> bool:
        """Method to locate user by email and check if pwd matches"""

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        """Method to take a user email and return a session id"""

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id


def _hash_password(Password: str) -> bytes:
    """Function to take in a str password and return bytes"""

    encode = Password.encode('utf-8')
    hashed = bcrypt.hashpw(encode, bcrypt.gensalt())

    return hashed


def _generate_uuid() -> str:
    """Function to create a new uuid"""

    return str(uuid.uuid4())
