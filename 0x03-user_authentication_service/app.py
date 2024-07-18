#!/usr/bin/env python3
"""
Flask application
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

AUTH = Auth()
app = Flask(__name__)

# Flask App
@app.route('/', methods=['GET'], strict_slashes=False)
def heymssg() -> str:
    """
    Welcome route that returns a JSON message.
    Returns a string:
        JSON
    Status Code: 200 (OK)
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def user() -> str:
    """
    User registration route.

    Returns(string):
        JSON response indicating success
    Status Code: 200 (OK) on success
    400 (Bad Request) on failure.
    """
    # email of the user
    email = request.form.get('email')
    # passwd of the user
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password) # register the user
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"messege": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    This route takes email and password from the request form
    User login route
    It attempts to validate the login credentials using the
    `Auth.valid_login` method.
    If the credentials are invalid, it returns a 401
    """
    # get the user info from thr form data
    email = request.form.get('email')
    password = request.form.get('password')
    # new user sess
    succsslogn = AUTH.valid_login(email, password)
    if not succsslogn:
        abort(401) # raises a 401 if ut fails
    session_id = AUTH.create_session(email)
    # resonse
    respns = jsonify({"email": f"{email}", "message": "logged in"})
    respns.set_cookie('session_id', session_id)
    return respns


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    User profile
    If a valid session is found
        it fetches the user's email from the session
        returns it in a JSON response,
        returns a 403 (Forbidden) status code otherwise
    Returns:
        JSON: A JSON obj with the user's email on success.
        Status Code: 200 (OK) on success
        403 (Forbidden) on fail
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403) # fail

@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    User log out
    This route retrieves the session ID from the request cookie.
    attempts to get the user object associated with the session ID
    using the `Auth.get_user_from_session_id` method.
    Returns:
        Redirect: Redirects to the welcome route on success.
        Status Code: 200 (OK) on success
        otherwise 403
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403) # if it fails 403



@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Initiates the password reset process.
    If a user with the
    provided email is found,
    a reset token is generated and sent to
    the user
    Returns:
        JSON: A JSON object with the user's email
        reset token on success.
        Status Code: 200 (OK) on success
    """
    email = request.form.get('email')
    user = AUTH.create_session(email)
    if not user:
        abort(403)
    else:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
    Update passwd
    It attempts to update the user's password using the
    `Auth.update_password` method
    Returns:
        JSON: A JSON obj with the user's email,
        success message on success.
        Status Code: 200 (OK) on success
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_psw = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_psw)
        return jsonify({"email": f"{email}",
                        "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
