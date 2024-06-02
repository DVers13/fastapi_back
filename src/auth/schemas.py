from typing import Optional

from fastapi_users import schemas

from pydantic import BaseModel
class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    role_id: int
    group_id: Optional[int]
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    email: str
    username: str
    password: str
    role_id: int
    group_id: Optional[int] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

class Group(BaseModel):
    id: int
    name: str
class GroupCreate(BaseModel):
    name: str

class RoleCreate(BaseModel):
    id: int
    name: str
    permissions: dict