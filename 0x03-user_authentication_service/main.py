#!/usr/bin/env python3
"""Main file for the advanced task"""

import requests

url = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Check the register user output"""

    response = requests.post(f"{url}/users", data={'email': email,
                                                   'password': password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    res = requests.post(f"{url}/users", data={'email': email,
                                              'password': password})
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Check what happens when you login with wrong password"""

    response = requests.post(f"{url}/sessions", data={'email': email,
                                                      'password': password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Check hat happens wher you login properly"""

    response = requests.post(f"{url}/sessions", data={'email': email,
                                                      'password': password})
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in response.cookies
    assert data["email"] == email
    assert data["message"] == "logged in"
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """What happens if you check profile when not logged in"""

    response = requests.get(f"{url}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """WHat hapens when you check profile normally"""

    cookies = {'session_id': session_id}
    response = requests.get(f"{url}/profile", cookies=cookies)
    assert response.status_code == 200
    assert response.json() == EMAIL


def log_out(session_id: str) -> None:
    """What happens when you log out"""

    cookies = {'session_id': session_id}
    response = requests.delete(f"{url}/sessions", cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Output when you reset password"""

    response = requests.post(f"{url}/reset_password", data={'email': email})
    assert response.status_code == 200
    data = response.json()
    assert "reset_token" in data
    return data["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """What happens when ypu update password"""

    response = requests.post(f"{url}/update_password",
                             data={'email': email, 'reset_token': reset_token,
                                   'new_password': new_password})
    assert response.status_code == 200
    assert response.json() == {"message": "password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
