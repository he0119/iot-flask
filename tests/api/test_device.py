""" Test Device API
"""
API_URL = '/api/devices'


def check_id_one_data(data):
    """ Check deivce data(id 1)
    """
    assert data['id'] == 1
    assert data['name'] == 'test'
    assert data['displayName'] == 'test'
    assert data['schema'][0] == {
        'name': 'test1',
        'displayName': 'test1',
        'dataType': 2,
        'show': True,
        'allowControl': False
    }
    assert data['schema'][1] == {
        'name': 'test2',
        'displayName': 'test2',
        'dataType': 2,
        'show': True,
        'allowControl': False
    }
    assert data['schema'][2] == {
        'name': 'control',
        'displayName': 'control',
        'dataType': 3,
        'show': True,
        'allowControl': True
    }


def test_get_device(client):
    """ Get device info.
    """
    res = client.get(API_URL)

    assert res.status_code == 200
    data = res.json[0]
    check_id_one_data(data)


def test_get_device_by_id(client):
    """ Get device info by id
    """
    res = client.get(f'{API_URL}?id=1')

    assert res.status_code == 200
    data = res.json
    check_id_one_data(data)


def test_get_device_by_wrong_id(client):
    """ Get device info using wrong id
    """
    res = client.get(f'{API_URL}?id=10')

    assert res.status_code == 404


def test_create_device(client):
    """ Create new device."""
    data = {
        'name': 'test1',
        'display_name': 'test1',
        'schema': {
            'test11': ['test11', 1, 1, 0],
            'test22': ['test22', 1, 1, 0],
        }
    }
    res = client.post(API_URL, data=data)

    assert res.status_code == 201
    assert res.json['id'] == 2
    assert res.json['name'] == 'test1'
    assert res.json['displayName'] == 'test1'
    assert res.json['schema'][0] == {
        'name': 'test11',
        'displayName': 'test11',
        'dataType': 1,
        'show': True,
        'allowControl': False
    }
    assert res.json['schema'][1] == {
        'name': 'test22',
        'displayName': 'test22',
        'dataType': 1,
        'show': True,
        'allowControl': False
    }


def test_modify_device(client):
    """ Modify device info.
    """
    data = {'id': 1, 'name': 'testt', 'display_name': 'testtt'}
    res = client.put(API_URL, data=data)

    assert res.status_code == 201

    res = client.get(f'{API_URL}?id=1')

    assert res.status_code == 200
    assert res.json['id'] == 1
    assert res.json['name'] == 'testt'
    assert res.json['displayName'] == 'testtt'


def test_modify_device_schema(client):
    """ Modify device schema
    """
    new_schema = {
        'test1': ['测试1', 2, 1, 0],
        'test2': ['测试2', 2, 1, 0],
        'control': ['控制', 3, 1, 1],
    }
    data = {'id': 1, 'schema': new_schema}
    res = client.put(API_URL, data=data)

    assert res.status_code == 201

    res = client.get(f'{API_URL}?id=1')

    assert res.status_code == 200
    assert res.json['id'] == 1
    assert res.json['name'] == 'test'
    assert res.json['displayName'] == 'test'
    assert res.json['schema'][0] == {
        'name': 'test1',
        'displayName': '测试1',
        'dataType': 2,
        'show': True,
        'allowControl': False
    }
    assert res.json['schema'][1] == {
        'name': 'test2',
        'displayName': '测试2',
        'dataType': 2,
        'show': True,
        'allowControl': False
    }
    assert res.json['schema'][2] == {
        'name': 'control',
        'displayName': '控制',
        'dataType': 3,
        'show': True,
        'allowControl': True
    }


def test_delete_device(client):
    """ Delete current user.
    """
    res = client.delete(API_URL, data={'id': 1})

    assert res.status_code == 204

    res = client.delete(API_URL, data={'id': 1})

    assert res.status_code == 404
