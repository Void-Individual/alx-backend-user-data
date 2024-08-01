#!/usr/bin/env python3
"""Function to return obfuscated log message"""

import re
from typing import List


# pattern = r'\b(' + '|'.join(fields) + r'[;]'
def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    pattern = r'|'.join(f'{field}=[^{separator}]+' for field in fields)
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}",
                  message)
