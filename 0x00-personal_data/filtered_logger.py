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
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
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


def main():
    """Logs the information about user records in a table.
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


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


if __name__ == "__main__":
    main()