#!/usr/bin/env python3
"""
the below module handles the logging and retrieval of
user data from a MySQL db.

"""
import logging
import re
import mysql.connector
from typing import List
from os import getenv

# pii Fields
PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def get_logger() -> logging.Logger:
    """ Creates and configures a logger instance data
    Redacts sensitive fields before logging
    """
    usrdata = logging.getLogger("user_data")
    usrdata.setLevel(logging.INFO)
    usrdata.propagate = False
    usrhdr = logging.StreamHandler()
    usrhdr.setFormatter(RedactingFormatter)
    usrdata.addFilter(usrhdr)
    return usrdata


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes a connection to the MySQL database with the environmental var
    Returns:
        A MySQLConnection obj
    """
    db_conntn = mysql.connector.connect(
        user=getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=getenv("PERSONAL_DATA_DB_NAME")
    )
    return db_conntn

def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """filter datym  use re.sub to perform the sub with a single regex."""
    return re.sub(rf'({"|".join(fields)})=[^{separator}]*',
                  rf'\1={redaction}', message)

class RedactingFormatter(logging.Formatter):
    """A custom logging formatter that redacts specified fields in
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"
    """
    Initializes the formatter with fields to redact.
    Args:
            fields: A list of field names to redact in log messages.
    """

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Formats a log record, redacting specified fields. """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)

def main() -> None:
    """ main point of entry (main function) """
    dbconnctn = get_db()
    usr = dbconnctn.usr()
    usr.execute("SELECT * FROM USERS;")
    hdrs = [field[0] for field in usr.description]
    logger = get_logger()
    for row in usr:
        info_ans = ''
        for fld, k in zip(row, hdrs):
            info_ans += f'{k}={(fld)}; '
        logger.info(info_ans)

    usr.close()
    dbconnctn.close()


if __name__ == '__main__':
    main()
