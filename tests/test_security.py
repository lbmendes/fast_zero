import pytest
from fastapi import HTTPException
from jwt import decode

from fast_zero.security import (
    SECRET_KEY,
    create_access_token,
    get_current_user,
)

pytest_plugins = ('pytest_asyncio',)


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp']  # Testa se o valor de exp foi adicionado ao token


@pytest.mark.asyncio()
async def test_token_without_without_sub_must_fail(session):
    data = {'test': 'test'}
    token = create_access_token(data)
    with pytest.raises(HTTPException):
        await get_current_user(session, token)


@pytest.mark.asyncio()
async def test_token_with_inexistent_user_must_fail(session):
    data = {'sub': 'test'}
    token = create_access_token(data)
    with pytest.raises(HTTPException):
        await get_current_user(session, token)


@pytest.mark.asyncio()
async def test_token_generated_by_other_key_must_fail(session):
    fake_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE3MTYwODc3ODksImV4cCI6NDA4Mjg0Mjk4OSwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSJ9.sdvQABdTtURPnhfMHbNrwikhyu677T4ogxKvSMYviM8'  # noqa: E501
    with pytest.raises(HTTPException):
        await get_current_user(session, fake_token)
