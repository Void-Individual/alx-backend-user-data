#!/usr/bin/env python3
"""Function to return obfuscated log message"""

import re


# pattern = r'\b(' + '|'.join(fields) + r'[;]'
def filter_datum(fields, redaction, message, separator):
    message = message.split(separator)
    fixed = [re.sub(log.split('=')[1], redaction, log)
             if (log.split('=')[0] in fields)
             else log for log in message]
    return f'{separator}'.join(fixed)
