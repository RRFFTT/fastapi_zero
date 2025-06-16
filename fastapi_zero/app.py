from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(title='My First API')
database = []  # provisorio para estudos


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


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session= Depends(get_session)):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                detail='Username already exists!',
                status_code=HTTPStatus.CONFLICT,
            )

        elif db_user.email == user.email:
            raise HTTPException(
                detail='Email already exists!', status_code=HTTPStatus.CONFLICT
            )

    db_user = User(**user.model_dump())

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 10,
    offset: int = 0,
    session = Depends(get_session)):

    users = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': users}


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def get_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuario não encontrado!'
        )

    user_with_id = database[user_id - 1]

    return user_with_id


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database))

    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuario não encontrado!'
        )

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def delete_users(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuario não encontrado!'
        )

    user_with_id = database[user_id - 1]

    del database[user_id - 1]

    return user_with_id
