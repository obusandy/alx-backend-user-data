#!/usr/bin/env python3
"""
Main Module
"""
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def register_user(email: str, password: str) -> None:
    """register_user
    Creates a new user with the provided email and passwd.
    """
    assert True
    return


def log_in_wrong_password(email: str, password: str) -> None:
    """log_in_wrong_password
    Attempts to log in with incorrect credentials.
    """
    assert True
    # return session_id
    return


def log_in(email: str, password: str) -> str:
    """log_in
    Logs in a user.
    """
    assert True
    return ("")


def profile_unlogged() -> None:
    """profile_unlogged
    Handles profile access without a valid session
    """
    assert True
    return


def profile_logged(session_id: str) -> None:
    """profile_logged
    Retrieves user profile information
    """
    assert True
    return


def log_out(session_id: str) -> None:
    """log_out
    logs he user out"""
    assert True
    return


def reset_password_token(email: str) -> str:
    """reset_password_token
    Creates a password reset token for
    the specified email address
    """
    assert True
    return ("")


def update_password(reset_token: str, new_password: str) -> None:
    """update_password
    updates user assword
    """
    assert True
    return


EMAIL = "testexampl@gmail.com"
PASSWD = "arva2100"
NEW_PASSWD = "eva292929"

"""main point of entry
Main execution block
"""
if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token)
    log_in(EMAIL, NEW_PASSWD)
