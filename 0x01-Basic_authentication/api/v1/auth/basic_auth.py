#!/usr/bin/env python3
"""Module containing the basicauth class"""

from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User

T = TypeVar('T', bound='User')


class BasicAuth(Auth):
    """Class that inherits from thr base Auth class"""

    def __init__(self) -> None:
        super().__init__()

    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """Returns the base 64 part of the authorization header for
        basic authentication purposes"""

        header = authorization_header
        if header:
            if isinstance(header, str):
                if header[0:6] == 'Basic ':
                    return header[6:]

        return None

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Method to return the decoded value of a base 64 str"""

        header = base64_authorization_header
        if header:
            if isinstance(header, str):
                try:
                    decodes_bytes = base64.b64decode(header)
                    decoded_str = decodes_bytes.decode('utf-8')
                    return decoded_str
                except (base64.binascii.Error, UnicodeDecodeError):
                    return None

        return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> Tuple[str, str]:
        """Method to retrieve and return user email and password from the
        base64 decoded value"""

        header = decoded_base64_authorization_header
        if header:
            if isinstance(header, str):
                if ':' in header:
                    email, pwd = header.split(':', maxsplit=1)
                    return (email, pwd)

        return (None, None)

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> T:
        """Method to return the user instance based on the email and pwd"""

        if user_email and isinstance(user_email, str):
            if user_pwd and isinstance(user_pwd, str):
                users = User.search({'email': user_email})
                if users is not None:
                    for user in users:
                        if user.is_valid_password(user_pwd) is True:
                            return user

        return None

    def current_user(self, request=None) -> T:
        """Overloads Auth and retrieves current user instance for a request"""
