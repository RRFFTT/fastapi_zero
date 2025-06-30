from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


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

    return_get = {'users': []}

    assert response.status_code == HTTPStatus.OK
    assert response.json() == return_get


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    return_get = {'users': [user_schema]}

    assert response.status_code == HTTPStatus.OK
    assert response.json() == return_get


def test_update_users(client, user):
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


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuário deletado!'}


def test_update_integrity_erro(client, user):
    # Inserindo fausto
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando usuario user

    response = client.put(
        f'users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'teste@test.com',
            'password': 'test123',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Nome de usuário ou email já cadastrados!'
    }


def test_create_username_integrity_erro(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'teste2@test.com',
            'password': 'test123456',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Nome de usuario ja cadastrado!'}


def test_create_mail_integrity_erro(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste2',
            'email': user.email,
            'password': 'test123456',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'E-mail já cadastrado!'}


def test_delete_user_should_return_not_found(client):
    response = client.delete('/users/333')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado!'}


def test_update_user_should_return_not_found(client):
    response = client.put(
        '/users/333',
        json={
            'username': 'fausto',
            'email': 'teste@test.com',
            'password': 'test123',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado!'}


def test_get_user_should_return_not_found(client):
    response = client.get('/users/333')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado!'}


def test_get_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }
