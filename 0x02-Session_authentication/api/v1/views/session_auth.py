#!/usr/bin/env python3
"""
The below module sets up the Flask application and
defines routes for user authentication
"""

from flask import Flask, abort, request, jsonify
from api.v1.app import auth
from models.user import User

app = Flask(__name__)

@app.route('/api/v1/auth_session/logout', methods=['DELETE'])
def auth_session_logout():
    """
    class auth_session_logout
    Handle user logout by destroying the session.
    Returns:
        Response: JSON response
    """
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200

@app.route('/api/v1/auth_session/login', methods=['POST'])
def auth_session_login():
    """
    Class auth_session_login
    Handle user login by creating a new session.

    Returns:
        Response: JSON response
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    usr = User.search({'email': email})

    if not usr:
        return jsonify({"error": "no user found for this email"}), 404

    if not usr.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(usr.id)

    """
    usr dict
    """
    user_dict = usr.to_json()

    """
    Returns: response
    """
    cookie_name = app.config.get('SESSION_NAME')
    respns = jsonify(user_dict)
    respns.set_cookie(cookie_name, session_id)

    return respns