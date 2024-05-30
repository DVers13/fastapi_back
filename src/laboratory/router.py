from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database import get_async_session
from laboratory.models import laboratory, discipline, subject, discipline_groups, discipline_teacher
from laboratory.schemas import *
from auth.models import user, group, role
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

# @router.get("/info_discipline_by_id")
# async def get_info_discipline_by_id(discipline_id: int, session: AsyncSession = Depends(get_async_session)):

#     query = select(discipline).where(discipline.c.id == discipline_id)
#     result = await session.execute(query)
#     discipline_row = result.mappings().first()

#     query = select(group.c.name, group.c.id).join(discipline_groups, discipline_groups.c.group_id == group.c.id).where(discipline_groups.c.discipline_id == discipline_id)
#     result = await session.execute(query)
#     groups = result.mappings().all()

#     query = select(subject.c.name).where(subject.c.id == discipline_row.subject_id)
#     result = await session.execute(query)
#     subject_name = result.mappings().first()
    
#     query = select(user.c.username, user.c.id).join(discipline_teacher, discipline_teacher.c.teacher_id == user.c.id).where(discipline_teacher.c.discipline_id == discipline_id)
#     result = await session.execute(query)
#     teachers = result.mappings().all()

#     return {
#         "id": discipline_row.id,
#         "name": subject_name.name,
#         "group_list": groups,
#         "teacher_list": teachers
#             }

@router.post("/add_discipline_groups") #, dependencies=[Depends(check_permissions(["write"]))]
async def add_discipline_groups(new_discipline_groups: DisciplineGroupCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(discipline_groups).values(**new_discipline_groups.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


# query = select(user.c.id, user.c.username).join(role, user.c.role_id == role.c.id).where(role.c.name == "teacher")
# @router.get("/discipline_by_id")
# async def get_discipline_by_id(discipline_id: int, session: AsyncSession = Depends(get_async_session)):
#     async with session.begin():
#         result = await session.execute(
#             select(discipline).options(
#                 selectinload(discipline.c.subject_id),
#                 selectinload(discipline.c.discipline_groups)
#             ).filter(discipline.c.id == discipline_id)
#         )
#         discipline_row = result.scalar_one_or_none()

#         if not discipline_row:
#             raise HTTPException(status_code=404, detail="Discipline not found")
#         print(discipline_row)
#         # Получение названия дисциплины и групп
#         discipline_name = discipline_row.subject.name
#         groups = [
#             {"id": group.id, "name": group.name}
#             for group in discipline_row.discipline_groups
#         ]

#         return {
#             "id": discipline_row.id,
#             "name": discipline_name,
#             "groups": groups
#         }

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