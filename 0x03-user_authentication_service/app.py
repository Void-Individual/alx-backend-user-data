#!/usr/bin/env python3
"""Module containing the flask app"""

from flask import Flask, jsonify, request, abort, make_response, redirect
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
def login():
    """Method to log in via the session id"""

    data = request.get_data().decode('utf-8').split('&')
    args = {arg.split('=')[0]: arg.split('=')[1] for arg in data}

    try:
        email = args.get('email')
        password = args.get('password')
        if not AUTH.valid_login(email, password):
            abort(401)
        session_id = AUTH.create_session(email)
        response = make_response(jsonify({"email": email,
                                          "message": "logged in"}))
        response.set_cookie("session_id", session_id)

    except (ValueError, NoResultFound):
        abort(401)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Method to find the user with the requested session id, if the
    user exists, destry the session and redirect to GET / else respomd with
    403 HTTP status"""

    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    # If no iser is found reapomd with forbidden
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Method to find a user's detail"""

    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        response = make_response({"email": user.email})
        return response, 200
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
