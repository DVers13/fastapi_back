from typing import List
from fastapi import Depends, HTTPException
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from sqlalchemy import select

from auth.manager import get_user_manager
from auth.models import User, role
from config import SECRET_AUTH

from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from fastapi_users.authentication import BearerTransport

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

cookie_transport = CookieTransport(cookie_max_age=3600) # для теста

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

def check_permissions(required_permissions: List[str]):
    async def dependency(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
        query = select(role).where(role.c.id == user.role_id)
        result = await session.execute(query)
        user_role = result.mappings().first()
        if not user_role:
            raise HTTPException(status_code=400, detail="Invalid role")
        
        user_permissions = user_role.permissions or []
        if not all(permission in user_permissions for permission in required_permissions):
            raise HTTPException(status_code=403, detail="Not enough permissions")
        
        return user
    return dependency