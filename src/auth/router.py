from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from auth.schemas import GroupCreate, RoleCreate
from auth.models import group, role, user
from auth.base_config import check_permissions


router = APIRouter(
    prefix="/group_role",
    tags=["Group and Role"]
)

@router.get("/test_perm", dependencies=[Depends(check_permissions(["write"]))])
async def test_perm():
    return {"status": "success"}

@router.post("/test_role")
async def add_test_role(session: AsyncSession = Depends(get_async_session)):
    new_role = {
        "id" : 2,
        "name" : "student",
        "permissions": ["write", "read"]
    }
    stmt = insert(role).values(**new_role)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.post("/add_group")
async def add_group(new_group: GroupCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(group).values(**new_group.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.post("/add_role")
async def add_role(new_role: RoleCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(role).values(**new_role.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.get("/get_all_group")
async def get_all_group(session: AsyncSession = Depends(get_async_session)):
    query = select(group)
    result = await session.execute(query)
    return result.mappings().all()

@router.get("/get_all_teachers")
async def get_all_teachers(session: AsyncSession = Depends(get_async_session)):
    query = select(user).join(role, user.c.role_id == role.c.id).where(role.c.id == 1)
    result = await session.execute(query)
    teachers = result.all()
    return [{"user_id": teacher.id, "user_name": teacher.username} for teacher in teachers]

