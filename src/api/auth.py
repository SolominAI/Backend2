from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import UserIdDep
from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])


@router.post('/register')
async def register_user(
        data: UserRequestAdd = Body(openapi_examples={
            'user1': {
                'summary': 'Пример 1',
                'value': {
                    'email': 'test1@example.ru',
                    'password': 'password123'

                }
            },
            'user2': {
                'summary': 'Пример 2',
                'value': {
                    'email': 'test2@example.ru',
                    'password': 'password456'
                }
            }
        })
):
    hashed_password = AuthService().hesh_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}


@router.post('/login')
async def login_user(
        response: Response,
        data: UserRequestAdd = Body(openapi_examples={
            'user1': {
                'summary': 'Пример 1',
                'value': {
                    'email': 'test1@example.ru',
                    'password': 'password123'
                }
            },
            'user2': {
                'summary': 'Пример 2',
                'value': {
                    'email': 'test2@example.ru',
                    'password': 'password456'
                }
            }
        }),
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hached_password(email=data.email)
        if not user or not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Неверный логин или пароль')
        access_token = AuthService().create_access_token({'user_id': user.id})
        response.set_cookie('access_token', access_token)
        return {"access_token": access_token}


@router.get('/me')
async def get_me(
        user_id: UserIdDep,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
    return user


@router.post('/logout')
async def logout_user(
    response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "OK"}
