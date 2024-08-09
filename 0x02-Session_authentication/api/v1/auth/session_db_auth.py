#!/usr/bin/env python3
"""Module to contain authentication class for session db"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid


class SessionDBAuth(SessionExpAuth):
    """Class to authenticate a session from a db"""

    def __init__(self) -> None:
        """Instantiation"""

        super().__init__()

    def create_session(self, user_id=None):
        """This now creates and stores a new instance of UserSession"""

        session_id = super().create_session(user_id)
        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Method to return the user_id by requesting usersession
        in the db based on session_id"""

        user_id = super().user_id_for_session_id(session_id)
        if user_id is not None:
            return user_id

        # If expired or not found in super, check db for session
        sessions = UserSession.search({'session_id': session_id})
        for session in sessions:
            if session.user_id is None:
                session.remove()
                return session.user_id
        return None

    def destroy_session(self, request=None):
        """Method to delete the usersession from db based on the session id
        from the request cookie"""

        if request:
            session_id = self.session_cookie(request)
            if session_id in self.user_id_by_session_id:
                # Remove from in-memory storage
                self.user_id_by_session_id.pop(session_id, None)
                # Remove from db
                sessions = UserSession.search({'session_id': session_id})
                for session in sessions:
                    session.remove()
                    return True
        return False
