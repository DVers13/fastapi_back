from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from auth.schemas import GroupCreate, RoleCreate
from auth.models import group, role


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