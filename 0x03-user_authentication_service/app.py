#!/usr/bin/env python3
"""
Basic Flask App
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
app.strict_slashes = False
AUTH = Auth()


@app.route('/')
def message() -> str:
    """Message"""
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'])
def users() -> str:
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({'email': email, 'message': 'user created'})
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    email = request.form.get('email')
    password = request.form.get('password')
    is_valid = AUTH.valid_login(email, password)
    if is_valid:
        session_id = AUTH.create_session(email)
        response = jsonify({'email': email, 'message': 'logged in'})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
    Return:
        - Redirects to home route.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
