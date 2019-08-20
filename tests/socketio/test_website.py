""" Test Website Socketio
"""


def test_website(client):
    """ Request data through socketio.
    """
    client.socketio.emit('website', {'type': 'request'})

    res = client.socketio.get_received()

    message_exist = False
    for message in res:
        if message['name'] == 'status':
            message_exist = True
            assert message['args'][0]['id'] == 1
            assert message['args'][0]['time'] == '2017-07-14T02:40:00+00:00'
            assert message['args'][0]['data'] == {
                'control': False,
                'test1': 10.0,
                'test2': 12.0
            }
    assert message_exist is True
