#!/usr/bin/env python3
"""
Regex-ing
"""
import re
import logging
from typing import List
import os
import mysql.connector


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
    """
        returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(RedactingFormatter(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
        Creates a connector to a database
    """
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_pwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME', '')
    conn = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return conn


def main() -> None:
    db = get_db()

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

db = get_db()
cursor = db.cursor()
cursor.execute("SELECT COUNT(*) FROM users;")
for row in cursor:
    print(row[0])
cursor.close()
db.close()