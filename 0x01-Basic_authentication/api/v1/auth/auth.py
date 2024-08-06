#!/usr/bin/env python3
"""Module to manage API authentication"""

from flask import request, Request
from typing import List, TypeVar, Optional
from models.user import User

T = TypeVar('T', bound='User')


class Auth:
    """Class to handle authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method to return true if path is not in list of excluded_paths"""

        if path is None or excluded_paths is None:
            return True
    
        if path in excluded_paths:
            return False

        if path[-1] != '/':
            slash_path = path + '/'
            if slash_path in excluded_paths:
                return False

        return True

    def authorization_header(self, request: Optional[Request] = None) -> Optional[str]:
        """Retrieve the Authorization header from a Flask request object.

        Args:
            request (Optional[Request]): The Flask request object.

        Returns:
            Optional[str]: The value of the Authorization header if present, otherwise None.
        """

        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> T:
        """This will contain the flask request object"""

        return None
