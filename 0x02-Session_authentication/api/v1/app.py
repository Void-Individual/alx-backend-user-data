#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.auth import Auth
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = getenv('AUTH_TYPE', None)
if auth == "basic_auth":
    auth = BasicAuth()
elif auth == "auth":
    auth = Auth()
elif auth == "session_auth":
    auth = SessionAuth()


@app.before_request
def before_request():
    """Method to """

    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/']
    # If authentication requirement is turned on
    if auth is not None:
        check = auth.require_auth(request.path, excluded_paths)
        # If path is not one of the above paths, require authentication
        if check is True:
            authorized = auth.authorization_header(request)
            session_cookie = auth.session_cookie(request)
            # If there is no authorization header, abort
            if not authorized and not session_cookie:
                abort(401)
            valid_user = auth.current_user(request)
            if not valid_user:
                abort(403)
            else:
                request.current_user = valid_user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized handler"""

    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def not_allowed(error) -> str:
    """Forbidden access"""

    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
