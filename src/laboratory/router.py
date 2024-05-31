from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database import get_async_session
from laboratory.models import laboratory, discipline, subject, discipline_groups, discipline_teacher
from laboratory.schemas import *
from auth.models import User, user, group, role
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

@router.delete("/delete_laboratory_by_id")
async def delete_laboratory_by_id(laboratory_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(laboratory).where(laboratory.c.id == laboratory_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.post("/add_discipline") #, dependencies=[Depends(check_permissions(["write"]))]
async def add_discipline(new_discipline: DisciplineCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(discipline).values(**new_discipline.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.post("/add_full_discipline") #, dependencies=[Depends(check_permissions(["write"]))]
async def add_full_discipline(new_discipline: DisciplineFullCreate, session: AsyncSession = Depends(get_async_session)):
    new_discipline_dict = new_discipline.model_dump()
    group_id_list = new_discipline_dict.pop("group_id_list")
    teacher_id_list = new_discipline_dict.pop("teacher_id_list")
    stmt = insert(discipline).values(**new_discipline_dict).returning(discipline.c.id)
    result = await session.execute(stmt)
    new_discipline_id = result.scalar()
    
    if group_id_list:
        group_stmt = insert(discipline_groups).values([
            {"group_id": group_id, "discipline_id": new_discipline_id}
            for group_id in group_id_list
        ])
        await session.execute(group_stmt)

    if teacher_id_list:
        teacher_stmt = insert(discipline_teacher).values([
            {"teacher_id": teacher_id, "discipline_id": new_discipline_id}
            for teacher_id in teacher_id_list
        ])
        await session.execute(teacher_stmt)
    await session.commit()
    return {"status": "success"}

@router.get("/get_full_discipline_for_teacher")
async def get_full_discipline_for_teacher(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    if not user.is_superuser and user.role_id != 1:
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource.")
    
    stmt = (
        select(discipline)
        .join(discipline_teacher, discipline.c.id == discipline_teacher.c.discipline_id)
        .join(subject, discipline.c.subject_id == subject.c.id)
        .where(discipline_teacher.c.teacher_id == user.id)
    )
    
    result = await session.execute(stmt)
    disciplines = result.mappings().all()

    response = []
    for disc in disciplines:
        group_stmt = (
            select(group)
            .join(discipline_groups, group.c.id == discipline_groups.c.group_id)
            .where(discipline_groups.c.discipline_id == disc.id)
        )
        group_result = await session.execute(group_stmt)
        groups = group_result.mappings().all()

        subject_stmt = select(subject).where(subject.c.id == disc.subject_id)
        subject_result = await session.execute(subject_stmt)
        subjects = subject_result.mappings().first()
        response.append(DisciplineResponse(
            discipline_id=disc.id,
            subject=subjects.name,
            groups=[Group(id=grp.id, name=grp.name) for grp in groups]
        ))

    return response

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

@router.get("/discipline_by_id")
async def get_discipline_by_id(discipline_id: int, session: AsyncSession = Depends(get_async_session)):

    query = select(discipline).where(discipline.c.id == discipline_id)
    result = await session.execute(query)
    discipline_row = result.mappings().first()

    query = select(group.c.name, group.c.id).join(discipline_groups, discipline_groups.c.group_id == group.c.id).where(discipline_groups.c.discipline_id == discipline_row.id)
    result = await session.execute(query)
    groups = result.mappings().all()

    query = select(subject.c.name).where(subject.c.id == discipline_row.subject_id)
    result = await session.execute(query)
    subject_name = result.mappings().first()
    
    return {
        "id": discipline_row.id,
        "name": subject_name.name,
        "group_list": groups,
            }

@router.get("/info_discipline_by_id")
async def get_info_discipline_by_id(discipline_id: int, session: AsyncSession = Depends(get_async_session)):

    query = select(discipline).where(discipline.c.id == discipline_id)
    result = await session.execute(query)
    discipline_row = result.mappings().first()

    query = select(group.c.name, group.c.id).join(discipline_groups, discipline_groups.c.group_id == group.c.id).where(discipline_groups.c.discipline_id == discipline_row.id)
    result = await session.execute(query)
    groups = result.mappings().all()

    query = select(subject.c.name).where(subject.c.id == discipline_row.subject_id)
    result = await session.execute(query)
    subject_name = result.mappings().first()
    
    query = select(user).join(discipline_teacher, discipline_teacher.c.teacher_id == user.c.id).where(discipline_teacher.c.discipline_id == discipline_row.id)
    result = await session.execute(query)
    teachers = result.mappings().all()
    teachers = [{"id": teach.id, "name": teach.username} for teach in teachers]

    query = select(laboratory).where(laboratory.c.discipline_id == discipline_row.id)
    result = await session.execute(query)
    laboratorys = result.mappings().all()

    return {
        "id": discipline_row.id,
        "name": subject_name.name,
        "group_list": groups,
        "teacher_list": teachers,
        "laboratory_list": laboratorys
            }

@router.delete("/delete_discipline_by_id")
async def delete_discipline_by_id(discipline_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(discipline).where(discipline.c.id == discipline_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.post("/add_discipline_groups") #, dependencies=[Depends(check_permissions(["write"]))]
async def add_discipline_groups(new_discipline_groups: DisciplineGroupCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(discipline_groups).values(**new_discipline_groups.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

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