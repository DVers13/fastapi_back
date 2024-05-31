from fastapi import FastAPI

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from laboratory.router import router as router_laboratory
from student_laboratory.router import router as router_student_laboratory
from auth.router import router as router_group_role
from edit_db.router import router as router_edit_db
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_laboratory)

app.include_router(router_student_laboratory)

app.include_router(router_group_role)

app.include_router(router_edit_db)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)