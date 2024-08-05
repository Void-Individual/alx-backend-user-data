#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views
from typing import NoReturn

app_views.strict_slashes = False


@app_views.route('/status', methods=['GET'])
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/')
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized')
def unauthorized() -> NoReturn:
    """
    GET /api/v1/unauthorized
    Return: The endpoint shoukd raise a 401 error using abort
    """

    abort(401)


@app_views.route('/forbidden')
def forbidden() -> NoReturn:
    """
    GET /api/v1/forbidden
    Return: The endpoint shoukd raise a 403 error using abort
    """

    abort(403)
