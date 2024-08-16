#!/usr/bin/env python3
"""Module containing the flask app"""

from flask import Flask, jsonify, request, abort, make_response
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def hello():
    """First Test method"""

    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """Method to register a new user"""

    data = request.get_data().decode('utf-8').split('&')
    args = {arg.split('=')[0]: arg.split('=')[1] for arg in data}

    email = args.get('email')
    password = args.get('password')
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"})

    return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def log_in():
    """Method to log in via the session id"""

    data = request.get_data().decode('utf-8').split('&')
    args = {arg.split('=')[0]: arg.split('=')[1] for arg in data}

    try:
        email = args.get('email')
        password = args.get('password')
        if not AUTH.valid_login(email, password):
            raise NoResultFound
        session_id = AUTH.create_session(email)
        response = make_response(jsonify({"email": email,
                                          "message": "logged in"}))
        response.set_cookie("session_id", session_id)

    except (ValueError, NoResultFound):
        abort(401)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
