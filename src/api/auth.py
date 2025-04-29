from fastapi import APIRouter

from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])


@router.post('/register')
async def register_user(
        data: UserRequestAdd,
):
    hashed_password = '1231245'
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        hotel = await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}
