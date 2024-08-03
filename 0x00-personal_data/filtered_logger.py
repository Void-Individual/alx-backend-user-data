#!/usr/bin/env python3
"""Function to return obfuscated log message"""

import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class to create a log of user data
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Instantiation"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Method to filter incoming log records"""
        message = record.getMessage()
        record.msg = filter_datum(self.fields, self.REDACTION, message,
                                  self.SEPARATOR)
        return super().format(record)


# pattern = r'\b(' + '|'.join(fields) + r'[;]'
def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    pattern = r'|'.join(f'{field}=[^{separator}]+' for field in fields)
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}",
                  message)


# Open the file and retrieve the first line without newline
with open('user_data.csv', 'r') as file:
    user_data = file.readline().strip()

#
PII_Data = ['name', 'email', 'phone', 'ssn', 'password']
PII_FIELDS = tuple(data for data in user_data.split(',') if data in PII_Data)

# print(PII_FIELDS)


def get_logger() -> logging.Logger:
    """function to create a logger"""

    logger = logging.Logger("user_data")
    # Set the logging level to info
    logger.setLevel(logging.INFO)
    # Do not propagate messages to other loggers
    logger.propagate = False
    # Create a StreamHandler
    handler = logging.StreamHandler()

    # Create and set redacting formatter
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger
