""" Website SocketIO
"""
from flask_login import current_user

from iot import socketio
from iot.common.auth import authenticated_only


@socketio.on('website')
@authenticated_only
def handle_website_event(msg):
    """ Handle request from website
    """
    if msg['type'] == 'request':
        devices = current_user.devices.all()
        for device in devices:
            socketio.emit('status',
                          device.latest_json_data(),
                          room=current_user.username)
