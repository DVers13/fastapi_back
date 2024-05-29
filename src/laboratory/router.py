from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from laboratory.models import laboratory, discipline, subject
from laboratory.schemas import *
from auth.models import User, group, role
from auth.base_config import check_permissions, current_user

router = APIRouter(
    prefix="/laboratory",
    tags=["Laboratory"]
)

@router.get("/laboratory_by_id")
async def get_laboratory_by_id(laboratory_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(laboratory).where(laboratory.c.id == laboratory_id)
    result = await session.execute(query)
    return result.mappings().all()

@router.get("/get_all_laboratory")
async def get_all_subject(session: AsyncSession = Depends(get_async_session)):
    query = select(laboratory)
    result = await session.execute(query)
    return result.mappings().all()

@router.post("/add_laboratory")
async def add_laboratory(new_laboratory: LaboratoryCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(laboratory).values(**new_laboratory.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.patch("/update_laboratory/") #, dependencies=[Depends(check_permissions(["write"]))]
async def update_discipline(laboratory_id: int, update_data: LaboratoryUpdate, session: AsyncSession = Depends(get_async_session)):
    update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    
    if not update_dict:
        raise HTTPException(status_code=400, detail="No data provided for update")
    
    if not update_dict:
        raise HTTPException(status_code=400, detail="No data provided for update")

    stmt = (
        update(laboratory)
        .where(laboratory.c.id == laboratory_id)
        .values(**update_dict)
    )

    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Discipline not found")

    return {"status": "success"}

@router.post("/add_discipline") #, dependencies=[Depends(check_permissions(["write"]))]
async def add_discipline(new_discipline: DisciplineCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(discipline).values(**new_discipline.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.patch("/update_discipline/") #, dependencies=[Depends(check_permissions(["write"]))]
async def update_discipline(discipline_id: int, update_data: DisciplineUpdate, session: AsyncSession = Depends(get_async_session)):
    update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    
    if not update_dict:
        raise HTTPException(status_code=400, detail="No data provided for update")
    
    if not update_dict:
        raise HTTPException(status_code=400, detail="No data provided for update")

    stmt = (
        update(discipline)
        .where(discipline.c.id == discipline_id)
        .values(**update_dict)
    )

    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Discipline not found")

    return {"status": "success"}

@router.get("/get_all_discipline")
async def get_all_subject(session: AsyncSession = Depends(get_async_session)):
    query = select(discipline)
    result = await session.execute(query)
    return result.mappings().all()

@router.get("/get_all_subject")
async def get_all_subject(session: AsyncSession = Depends(get_async_session)):
    query = select(subject)
    result = await session.execute(query)
    return result.mappings().all()

@router.post("/add_subject")
async def add_subject(new_subject: Annotated[SubjectCreate, Depends()], session: AsyncSession = Depends(get_async_session)):
    stmt = insert(subject).values(**new_subject.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}