import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("k0t@pes.com", "1234", 200),
        ("k0t@pes.com", "1234", 409),
        ("k0t2@pes.com", "12345", 200),
        ("abc", "123456", 422),
        ("abc@abc", "123456", 422),
    ],
)
async def test_auth_flow(email: str, password: str, status_code: int, ac):
    # /register
    resp_register = await ac.post("/auth/register", json={"email": email, "password": password})
    assert resp_register.status_code == status_code
    if status_code != 200:
        return

    # /login
    resp_login = await ac.post("/auth/login", json={"email": email, "password": password})
    assert resp_login.status_code == 200
    assert "access_token" in ac.cookies
    assert "access_token" in resp_login.json()

    # /me
    resp_me = await ac.get("/auth/me")
    assert resp_me.status_code == 200
    user = resp_me.json()
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    # /logout
    resp_logout = await ac.post("/auth/logout")
    assert resp_logout.status_code == 200

    assert "access_token" not in ac.cookies
