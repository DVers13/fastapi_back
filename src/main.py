from fastapi import APIRouter, FastAPI, Depends
import uvicorn

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from laboratory.router import router as router_laboratory
from auth.models import User
from student_laboratory.router import router as router_student_laboratory
from auth.router import router as router_group_role
from edit_db.router import router as router_edit_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Nice App",
              description="API_DESC",
              version="0.2.0",
              docs_url='/api/docs',
              redoc_url='/api/redoc',
              openapi_url='/api/openapi.json')

api_router = APIRouter(prefix="/api")

api_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

api_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


####
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

current_user = fastapi_users.current_user()

@router.get("/me", response_model=UserRead)
async def get_me(user: User = Depends(current_user)):
    return user
####


api_router.include_router(router)
api_router.include_router(router_laboratory)
api_router.include_router(router_student_laboratory)
api_router.include_router(router_group_role)
api_router.include_router(router_edit_db)

app.include_router(api_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run('main:app', workers=4)