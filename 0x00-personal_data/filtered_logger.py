#!/usr/bin/env python3
"""Function to return obfuscated log message"""

import re
from typing import List
import logging
import os
from mysql import connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def main() -> None:
    """Function to obtain a db connection using get_db, retrieve all the rows
    in the users table and display each row under a filtered format"""

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')

    logger = get_logger()
    for row in cursor:
        x = ";".join([f"{field}={value}" for field, value
                     in zip(cursor.column_names, row)])
        message = f"{x};"

        args = ("user_data", logging.INFO, None, None, message, None, None)
        log_record = logging.LogRecord(*args)
        logger.handle(log_record)
    cursor.close()
    db.close()


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


def get_db() -> connector.connection.MySQLConnection:
    """Function to return a connector to a database"""

    # Use environment variables with default values
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME', 'holberton')

    return connector.connect(
        host=host,
        user=username,
        password=password,
        database=db_name
    )


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Method to return obfuscated log message"""
    pattern = r'|'.join(f'{field}=[^{separator}]+' for field in fields)
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}",
                  message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class to create a log of user data"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Instantiation while initializig the parent class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Method to filter incoming log records"""
        message = record.getMessage()
        record.msg = filter_datum(self.fields, self.REDACTION, message,
                                  self.SEPARATOR)
        return super().format(record)


if __name__ == "__main__":
    main()
