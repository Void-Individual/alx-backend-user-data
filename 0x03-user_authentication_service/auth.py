#!/usr/bin/env python3
"""Module for authentication"""

import bcrypt
import uuid
from db import DB
from user import User
from typing import Optional
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


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

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """If session_id is none or no user is found reurn none else return
        the corresponding user"""

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Method to update corresponding user"""

        try:
            user = self._db.find_user_by(user_id=user_id)
            self._db.update_user(user_id, session_id=None)
        except (NoResultFound, InvalidRequestError):
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Method tofind the user corresponding to the email, generate
        uuid and update the users reset_token db field then return the token,
        else raise a valueerror exception"""

        try:
            user = self._db.find_user_by(email=email)
            new_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=new_token)
            return new_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Use reset_token to fidn the corresponding user. If it doesn't
        exist, raise ValueError, otherwise hash the password, change the
        user password field and change the reset token field to None"""

        try:
            user = self._db.find_user_by(reset_token=reset_token)
            pwd = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=pwd,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError


def _hash_password(Password: str) -> bytes:
    """Function to take in a str password and return bytes"""

    encode = Password.encode('utf-8')
    hashed = bcrypt.hashpw(encode, bcrypt.gensalt())

    return hashed


def _generate_uuid() -> str:
    """Function to create a new uuid"""

    return str(uuid.uuid4())
