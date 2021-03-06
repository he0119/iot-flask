""" Test Status API
"""
API_URL = '/api/status'


def test_get_status(client):
    """ Get latest data.
    """
    res = client.get(API_URL)

    assert res.status_code == 200
    assert res.json[0]['id'] == 1
    assert res.json[0]['time'] == '2017-07-14T02:40:00+00:00'
    assert res.json[0]['data'] == {
        'test1': 10,
        'test2': 12,
        'control': False,
    }


def test_add_status(client):
    """ Add new device data.
    """
    data = {
        'id': 1,
        'time': 1500000010,
        'data': '12, 22, 1',
    }
    res = client.post(API_URL, data=data)

    assert res.status_code == 201
    assert res.json['message'] == 'Data2017-07-14 02:40:10 added'

    res = client.post(API_URL, data=data)

    assert res.status_code == 409
    assert res.json['message'] == 'Data already exist'

    res = client.get(API_URL)

    assert res.status_code == 200
    assert res.json[0]['id'] == 1
    assert res.json[0]['time'] == '2017-07-14T02:40:10+00:00'
    assert res.json[0]['data'] == {
        'test1': 12.0,
        'test2': 22.0,
        'control': True,
    }


def test_modify_device(client):
    """ Modify device status.
    """
    data = {
        'id': 1,
        'data': {
            'test1': 1,
        }
    }
    res = client.put(API_URL, data=data)

    assert res.status_code == 201

    res = client.socketio.get_received()

    message_exist = False
    for message in res:
        if message['name'] == '1':
            message_exist = True
            assert message['args'][0] == {'control': 'null'}
    assert message_exist is True

    data = {
        'id': 1,
        'data': {
            'test1': 1,
            'control': False,
        }
    }
    res = client.put(API_URL, data=data)

    assert res.status_code == 201

    res = client.socketio.get_received()

    message_exist = False
    for message in res:
        if message['name'] == '1':
            message_exist = True
            assert res[0]['args'][0] == {'control': False}
    assert message_exist is True
