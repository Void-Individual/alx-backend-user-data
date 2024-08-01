#!/usr/bin/env python3
"""Function to return obfuscated log message"""

import re

# pattern = r'\b(' + '|'.join(fields) + r'[;]'
def filter_datum(fields, redaction, message, separator):
    """
    fields: a list of str's representing all fields to obfuscate
    redaction: the replacement str
    message: a string representing the log line with data
    separator: The field separator of the log line
    """
    message = message.split(';')
    fixed = [re.sub(log.split('=')[1], redaction, log)
             if (log.split('=')[0] in fields)
             else log for log in message]
    return ';'.join(fixed)
