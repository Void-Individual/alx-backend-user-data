#!/usr/bin/env python3
"""Function to return obfuscated log message"""

import re


# pattern = r'\b(' + '|'.join(fields) + r'[;]'
def filter_datum(fields, redaction, message, separator):
    pattern = r'|'.join(f'{field}=[^{separator}]+' for field in fields)
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}",
                  message)
