#!/usr/bin/env python3
"""
Regex-ing
"""
import re
import logging
from typing import List


PII_FIELDS = (
    "name", "email", "phone", "ssn", "password"
)

def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
        Returns the log message obfuscated
    """
    pattern = f"({'|'.join(map(re.escape, fields))})=.*?{re.escape(separator)}"
    return re.sub(
        pattern, lambda m: f"{m.group(1)}={redaction}{separator}", message
    )

def get_logger() -> logging.Logger:
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(RedactingFormatter(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """Initialization"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters incoming log records using the filter_datum function.
        """
        record.msg = (filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR))
        return super(RedactingFormatter, self).format(record)
