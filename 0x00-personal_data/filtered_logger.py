#!/usr/bin/env python3
"""
Regex-ing
"""
import re


def filter_datum(fields, redaction, message, separator) -> str:
    """
        Returns the log message obfuscated
    """
    pattern = f"({'|'.join(map(re.escape, fields))})=.*?{re.escape(separator)}"
    return re.sub(
        pattern, lambda m: f"{m.group(1)}={redaction}{separator}", message
    )
