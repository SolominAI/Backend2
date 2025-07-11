from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import ObjectAlreadyExistsException
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserRequestAdd = Body(
        openapi_examples={
            "user1": {
                "summary": "Пример 1",
                "value": {"email": "test1@example.ru", "password": "password123"},
            },
            "user2": {
                "summary": "Пример 2",
                "value": {"email": "test2@example.ru", "password": "password456"},
            },
        }
    ),
):
    try:
        hashed_password = AuthService().hesh_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        await db.users.add(new_user_data)
        await db.commit()

    except ObjectAlreadyExistsException:
        raise HTTPException(status_code=409, detail="Пользователь с такой почтой уже существует")

    return {"status": "OK"}


@router.post("/login")
async def login_user(
    db: DBDep,
    response: Response,
    data: UserRequestAdd = Body(
        openapi_examples={
            "user1": {
                "summary": "Пример 1",
                "value": {"email": "test1@example.ru", "password": "password123"},
            },
            "user2": {
                "summary": "Пример 2",
                "value": {"email": "test2@example.ru", "password": "password456"},
            },
        }
    ),
):
    user = await db.users.get_user_with_hached_password(email=data.email)
    if not user or not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout_user(
    response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "OK"}
