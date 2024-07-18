#!/usr/bin/env python3
"""
module initializes and configures the Flask app
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


""" Flask app"""
app = Flask(__name__)
# Register the blueprint for API routes
app.register_blueprint(app_views)
# Enable CORS
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
if os.getenv('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif os.getenv('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """
    status code for a request unauthorized
    404 of course
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    status code for a request unauthorized
    401 of course
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    status code for a request where the user is
    authenticated but not allowed to access to a resource
    Returns a JSON response with an err msg
    403 status code.
    """
    return jsonify({"error": "Forbidden"}), 403


# Perform authentication
@app.before_request
def before_request() -> None:
    """
    Perform operations before any route is handled.
    Checks if the request path requires authentication
    """
    paths = ['/api/v1/status/', '/api/v1/unauthorized/',
             '/api/v1/forbidden/']
    if not auth:
        return None
    if not auth.require_auth(request.path, paths):
        return None
    if not auth.authorization_header(request):
        abort(401)
    if not auth.current_user(request):
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
