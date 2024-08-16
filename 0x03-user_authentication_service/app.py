#!/usr/bin/env python3
"""Module containing the flask app"""

from flask import Flask, jsonify, request
from auth import Auth

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
    args = {}
    for arg in data:
        arg = arg.split('=')
        args[arg[0]] = arg[1]

    email = args.get('email')
    password = args.get('password')
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"})

    return jsonify({"email": email, "message": "user created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
