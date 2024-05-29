from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from auth.schemas import GroupCreate, RoleCreate
from auth.models import group, role, user


router = APIRouter(
    prefix="/group_role",
    tags=["Group and Role"]
)

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
    query = select(user.c.id, user.c.username).join(role, user.c.role_id == role.c.id).where(role.c.name == "teacher")
    result = await session.execute(query)
    teachers = result.all()
    return [{"user_id": teacher.id, "user_name": teacher.username} for teacher in teachers]