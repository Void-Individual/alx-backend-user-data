#!/usr/bin/env python3
"""Function to return obfuscated log message"""

import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
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
