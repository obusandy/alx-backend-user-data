#!/usr/bin/env python3
""" the below is a model where pass is encrypted """
import bcrypt

def hash_password(password: str) -> bytes:
    """ bycrypt
    Hashes a password using bcrypt.
    Returns:
        bytes: The hashed password."""
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())

def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Validates a password against a hashed password using bcrypt

    Returns:
        bool: True if the password matches the hashed password,
        False incase otherwise"""
    password = password.encode()
    if bcrypt.checkpw(password, hashed_password):
        return True
    return False