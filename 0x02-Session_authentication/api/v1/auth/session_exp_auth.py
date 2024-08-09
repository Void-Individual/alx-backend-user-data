#!/usr/bin/env python3
"""Module for session authentication with expiration"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """A session class with an expiration time"""

    def __init__(self) -> None:
        """Instantiation overload"""

        super().__init__()
        timer = getenv('SESSION_DURATION', None)
        if timer is None or timer == '':
            self.session_duration = 0
        else:
            try:
                self.session_duration = int(timer)
            except ValueError:
                self.session_duration = 0

    def create_session(self, user_id=None):
        """Method to overload and continue the creation of session_id"""

        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overload this method from the parent"""

        if session_id:
            if session_id in self.user_id_by_session_id.keys():
                session_dict = self.user_id_by_session_id[session_id]
                created = session_dict.get('created_at')
                user_id = session_dict.get('user_id')
                if self.session_duration <= 0:
                    return user_id
                if not created:
                    return None
                # Add the session duration to the created time
                expired = created + timedelta(seconds=self.session_duration)
                if datetime.now() > expired:
                    return None
                return user_id

        return None
