#!/usr/bin/env python3
"""Module containing session auth class"""

import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """CLass containging details for authenticating a users cureent session"""

    def __init__(self) -> None:
        """Instantiate any super attributes"""
        self.user_id_by_session_id = {}
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """Method that creates a Session ID for a user_id"""

        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = uuid.uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Method that returns a User ID based on a Session ID"""

        session_id = str(session_id)
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id, None)
        return user_id
