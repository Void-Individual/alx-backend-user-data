#!/usr/bin/env python3
"""Module to manage API authentication"""

from flask import request
from typing import List, TypeVar
from models.user import User

T = TypeVar('T', bound='User')


class Auth:
    """Class to handle authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method to return true or false"""

        return False

    def authorization_header(self, request=None) -> str:
        """This will contain the flask request object"""

        return None

    def current_user(self, request=None) -> T:
        """This will contain the flask request object"""

        return None
