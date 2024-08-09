#!/usr/bin/env python3
"""Module to store user sessions"""

from models.base import Base


class UserSession(Base):
    """CLass that inherits from base to store user sessions"""

    def __init__(self, *args: list, **kwargs: dict):
        """Instantiation"""

        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
