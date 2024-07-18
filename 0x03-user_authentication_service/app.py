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


@app.route('/profile', methods=['GET'])
def profile():
    """
        Find a user using a session_id cookie obtained from the user request
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    print(user)
    if user:
        return jsonify({'email': user.email})
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def reset_password():
    """
        Get a reset password token
    """
    email = request.form.get('email')
    try:
        user = AUTH._db.find_user_by(email=email)
        reset_token = AUTH.get_reset_password_token(email)
        response = jsonify({'email': email, 'reset_token': reset_token})
        return response, 200
    except NoResultFound:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def reset_password():
    """
        Update Password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        user = AUTH._db.find_user_by(reset_token=reset_token, email=email)
    except NoResultFound:
        abort(403)
    AUTH.update_password(reset_token, new_password)
    return jsonify({'email': email, 'message': 'Password updated'}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
