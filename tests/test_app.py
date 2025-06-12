from http import HTTPStatus


def test_root_return_ola_mundo(client):
    response = client.get('/')
    assert response.json() == {'message': 'Olá, mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_html_response(client):
    response = client.get('/html-response')

    html_assert = """
            <html>
                <head>
                    <title>Exercicio 02 - Retorno HTML</title>
                </head>
                <body>
                    <h3>Olá, mundo!<br> Este é o retorno com HTML puro.<br>
                    </h3>
                </body>
            </html>
            """

    assert response.status_code == HTTPStatus.OK
    assert response.text == html_assert


def test_create_user(client):
    payload = {
        'username': 'alice',
        'password': 'secret',
        'email': 'alice@paradiseword.com',
    }

    response = client.post('/users', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@paradiseword.com',
        'username': 'alice',
    }


def test_read_users(client):
    response = client.get('/users/')

    return_get = {
        'users': [
            {'username': 'alice', 'email': 'alice@paradiseword.com', 'id': 1}
        ]
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json() == return_get


def test_get_user(client):
    response = client.get('/users/1')

    expected_response = {
        'id': 1,
        'email': 'alice@paradiseword.com',
        'username': 'alice',
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response

    response_exception = client.get('/users/2')

    expected_response = {'detail': 'Usuario não encontrado!'}

    assert response_exception.status_code == HTTPStatus.NOT_FOUND
    assert response_exception.json() == expected_response


def test_put_users(client):
    payload = {
        'username': 'bob',
        'email': 'bob@paradiseword.com',
        'password': 'secret',
    }

    response = client.put('/users/1', json=payload)

    expected_response = {
        'id': 1,
        'username': 'bob',
        'email': 'bob@paradiseword.com',
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response

    response_exception = client.put('/users/0', json=payload)

    expected_response = {'detail': 'Usuario não encontrado!'}

    assert response_exception.status_code == HTTPStatus.NOT_FOUND
    assert response_exception.json() == expected_response


def test_delete_user(client):
    response = client.delete('/users/1')

    expected_response = {
        'id': 1,
        'username': 'bob',
        'email': 'bob@paradiseword.com',
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response

    response_exception = client.delete('/users/2')

    expected_response = {'detail': 'Usuario não encontrado!'}

    assert response_exception.status_code == HTTPStatus.NOT_FOUND
    assert response_exception.json() == expected_response
