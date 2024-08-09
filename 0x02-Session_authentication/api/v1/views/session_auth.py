#!/usr/bin/env python3
"""Module to handle routes for session authentication"""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def session_login() -> str:
    """
    Method to handle session authentication
    usage: POST /auth_session/login
    Return:
        A response containing:
            - Valid user that matches the email passed
            - Set cookies with the session_id
    """

    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        checked = user.is_valid_password(password)
        if checked:
            break
        user = None
    if not user:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = make_response(user.to_json())
    response.set_cookie(getenv('SESSION_NAME'), session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> None:
    """Method to delete the session id containing the request as a cookie"""

    from api.v1.app import auth
    logout = auth.destroy_session(request)
    if not logout:
        abort(404)
    return jsonify({}), 200
