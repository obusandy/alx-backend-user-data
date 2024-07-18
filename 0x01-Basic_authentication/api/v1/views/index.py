#!/usr/bin/env python3
"""
module defines routes for status checking, statistics,
and handling
unauthorized and forbidden requests for the API.
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
     Returns a JSON response with a status of "OK"
     Means the Api is up
        Response: JSON response indicating the status.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """
    Returns a JSON response containing the count of
    various objts in the system.
    Returns:
        Respns: JSON response with statistics
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """
    status code for a request unauthorized 401 of course
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """
    status code for a request where the user is authenticate
    but not allowed to access to a resource
    """
    abort(403)
