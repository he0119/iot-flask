""" Authentication
"""
import functools
import json

from flask import Response, current_app
from flask_jwt_extended import current_user as jwt_current_user
from flask_jwt_extended import verify_jwt_in_request
from flask_login import current_user
from flask_socketio import disconnect, emit, join_room

from iot import jwt, login_manager, socketio
from iot.models.user import User

# From https://flask-socketio.readthedocs.org/en/latest/


@socketio.on('connect')
def connect_handler():
    """ Add device into room
    """
    if current_user.is_authenticated:
        join_room(current_user.username)
        emit('info', {'message': 'A new client has joined'},
             room=current_user.username)
    else:
        return False  # not allowed here


def authenticated_only(func):
    """ Only allow authenticated user to connect socketio
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        return func(*args, **kwargs)

    return wrapped


@login_manager.request_loader
def load_user_from_request(request):
    """ Load user for flask login.
    """
    auth = request.authorization
    # try to authenticate with username/password
    if auth:
        user = User.query.filter_by(username=auth.username).first()
        if not user or not user.check_password(auth.password):
            return None
        return user

    # try to authenticate with JWT Token
    jwt_header = request.headers.get(current_app.config['JWT_HEADER_NAME'],
                                     None)
    if jwt_header and current_app.config['JWT_HEADER_TYPE'] in jwt_header:
        # Verify JWT Token
        verify_jwt_in_request()
        return jwt_current_user

    # finally, return None if there isn't auth
    return None


@login_manager.unauthorized_handler
def unauthorized_handler():
    """ Handle unauthorized request.
    """
    message = {'message': 'You have to login with proper credentials'}
    return Response(json.dumps(message), 401)


@jwt.user_loader_callback_loader
def jwt_user_loader(username):
    """ Return user based on username.
    """
    return User.query.filter_by(username=username).first()
