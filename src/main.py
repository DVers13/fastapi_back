from fastapi import FastAPI

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from laboratory.router import router as router_laboratory
from student_laboratory.router import router as router_student_laboratory
from auth.router import router as router_group_role

app = FastAPI(
    title="Nice App"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_laboratory)

app.include_router(router_student_laboratory)

app.include_router(router_group_role)