#!/usr/bin/env python3
"""
The below module sets up the Flask application and
defines routes for user authentication
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    class auth_session_logout
    Handle user logout by destroying the session.
    Returns:
        Response: JSON response
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
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
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for usr in users:
        if not usr.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        from api.v1.app import auth
        session_id = auth.create_session(usr.id)
        respns = jsonify(usr.to_json())
        respns.set_cookie(getenv('SESSION_NAME'), session_id)
        return respns
    return jsonify({"error": "no user found for this email"}), 404
