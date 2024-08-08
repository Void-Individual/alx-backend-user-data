#!/usr/bin/env python3
"""Module containing session auth class"""

import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """CLass containging details for authenticating a users cureent session"""

    user_id_by_session_id = {}

    def __init__(self) -> None:
        """Instantiate any super attributes"""
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """Method that creates a Session ID for a user_id"""

        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = uuid.uuid4()
        self.user_id_by_session_id[str(session_id)] = user_id
        return str(session_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Method that returns a User ID based on a Session ID"""

        # session_id = str(session_id)
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id, None)
        return user_id

    def current_user(self, request=None):
        """An overloading method to return a user instance based on a cookie
        value passed in the request"""

        if request:
            session_cookie = self.session_cookie(request)
            if session_cookie:
                user_id = self.user_id_for_session_id(session_cookie)
                return User.get(user_id)

        return None
