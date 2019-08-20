""" Test Device Socketio
"""


def test_add_devicedata(client):
    """ Add data through socketio.
    """
    client.socketio.emit('devicedata', {'data': '1500000010,1|12,22,1'})

    res = client.socketio.get_received()

    message_exist = False
    for message in res:
        if message['name'] == 'status':
            message_exist = True
            assert message['args'][0]['id'] == 1
            assert message['args'][0]['time'] == '2017-07-14T02:40:10+00:00'
            assert message['args'][0]['data'] == {
                'control': True,
                'test1': 12.0,
                'test2': 22.0
            }
    assert message_exist is True


def test_add_devicedata_jwt(client):
    """ Add data through socketio by jwt client.
    """
    client.socketio_jwt.emit('devicedata', {'data': '1500000010,1|12,22,1'})

    res = client.socketio_jwt.get_received()

    message_exist = False
    for message in res:
        if message['name'] == 'status':
            message_exist = True
            assert message['args'][0]['id'] == 1
            assert message['args'][0]['time'] == '2017-07-14T02:40:10+00:00'
            assert message['args'][0]['data'] == {
                'control': True,
                'test1': 12.0,
                'test2': 22.0
            }
    assert message_exist is True
