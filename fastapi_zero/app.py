from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastapi_zero.schemas import Message, UserSchema, UserPublic

app = FastAPI(title='My First API')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá, mundo!'}

@app.get(
    '/html-response', response_class=HTMLResponse, status_code=HTTPStatus.OK
)
def htmlpage():
    return """
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


@app.post('/users/',
          status_code=HTTPStatus.CREATED,
          response_model=UserPublic)

def create_user(user:UserSchema):
    return user
