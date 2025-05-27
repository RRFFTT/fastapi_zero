from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root_return_ola_mundo():
    client = TestClient(app)

    response = client.get('/')
    assert response.json() == {'message': 'Olá, mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_html_response():
    client = TestClient(app)

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
