from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from laboratory.models import laboratory, discipline
from laboratory.schemas import LaboratoryCreate, DisciplineCreate
from auth.models import User, group, role
from auth.base_config import check_permissions, current_user


router = APIRouter(
    prefix="/laboratory",
    tags=["Laboratory"]
)

@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_user)):
    return {"message": f"Hello {user}!"}


@router.get("/", dependencies=[Depends(check_permissions(["read"]))])
async def get_laboratory_by_id(laboratory_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(laboratory).where(laboratory.c.id == laboratory_id)
    result = await session.execute(query)
    return result.all()

@router.post("/", dependencies=[Depends(check_permissions(["write"]))])
async def add_laboratory(new_laboratory: LaboratoryCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(laboratory).values(**new_laboratory.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.post("/discipline")
async def add_discipline(new_discipline: DisciplineCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(discipline).values(**new_discipline.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}