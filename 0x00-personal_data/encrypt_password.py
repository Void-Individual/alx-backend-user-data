#!/usr/bin/env python3
"""Module to encrypt a password"""

import bcrypt


def hash_password(pwd: str) -> bytes:
    """Function to encrypt a str into a salted, hashed password
    in the form of a byte string"""

    # You encode the pwd from its unicode format to bytes
    # You generate the salt, whiuch is a byte string
    hash = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
    return hash


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Function to validate that the provuded password matches the hashed
    password and returns true or false"""

    # You cannot decrypt an already hashed str, you can only compare
    valid = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    return valid
