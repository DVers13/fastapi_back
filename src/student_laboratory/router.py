from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, delete, select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from auth.models import User
from laboratory.models import discipline_teacher, laboratory
from student_laboratory.models import student_laboratory
from student_laboratory.schemas import StudentLaboratoryCreate, StudentLaboratoryUpdate
from auth.base_config import check_permissions, current_user
router = APIRouter(
    prefix="/student_laboratory",
    tags=["student_laboratory"]
)

@router.get("/get_student_laboratory_by_id")
async def get_student_laboratory_by_id(student_laboratory_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(student_laboratory).where(student_laboratory.c.id == student_laboratory_id)
    result = await session.execute(query)
    return result.all()

@router.get("/get_all_student_laboratory_for_teacher", dependencies=[Depends(check_permissions(["get_student_laboratory_for_teacher"]))])
async def get_student_laboratory_for_teacher(user: User = Depends(current_user),
                                        session: AsyncSession = Depends(get_async_session),
                                        is_personally: bool = Query(False)):
    teacher_id = user.id
    labs_without_teacher = []

    filters = [student_laboratory.c.status == False, student_laboratory.c.valid == True]
    # if status is not None:
    #     filters.append(student_laboratory.c.status == status) status: bool = Query(None), в get_student_laboratory_for_teacher в конец
    # if valid is not None:
    #     filters.append(student_laboratory.c.valid == valid)
    # if min_score is not None:
    #     filters.append(student_laboratory.c.score >= min_score)
    # if max_score is not None:
    #     filters.append(student_laboratory.c.score <= max_score)

    query_with_teacher = select(student_laboratory).where(student_laboratory.c.id_teacher == teacher_id)
    if not is_personally:
        query_without_teacher = select(student_laboratory).join(laboratory, laboratory.c.id == student_laboratory.c.id_lab).where(student_laboratory.c.id_teacher.is_(None))
        query_without_teacher = query_without_teacher.where(and_(*filters))
        result_disciplines = await session.execute(select(discipline_teacher.c.discipline_id).where(discipline_teacher.c.teacher_id == teacher_id))
        discipline_ids = [row.discipline_id for row in result_disciplines]
        query_without_teacher = query_without_teacher.where(laboratory.c.discipline_id.in_(discipline_ids))
        result_without_teacher = await session.execute(query_without_teacher)
        labs_without_teacher = result_without_teacher.mappings().all()

    query_with_teacher = query_with_teacher.where(and_(*filters))

    result_with_teacher = await session.execute(query_with_teacher)
    labs_with_teacher = result_with_teacher.mappings().all()

    all_labs = labs_with_teacher + labs_without_teacher
    sorted_labs = sorted(all_labs, key=lambda lab: lab['id'])
    return sorted_labs

@router.post("/add_student_laboratory")
async def add_student_laboratory(new_student_laboratory: Annotated[StudentLaboratoryCreate, Depends()], user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    new_student_laboratory_dict = new_student_laboratory.model_dump()
    new_student_laboratory_dict["id_student"] = user.id
    new_student_laboratory_dict["status"] = False
    new_student_laboratory_dict["score"] = "0"
    new_student_laboratory_dict["count_try"] = 0
    new_student_laboratory_dict["valid"] = True
    stmt = insert(student_laboratory).values(**new_student_laboratory_dict)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

# @router.patch("/update_student_laboratory/") #, dependencies=[Depends(check_permissions(["write"]))]
# async def update_student_laboratory(student_laboratory_id: int, update_data: StudentLaboratoryUpdate, session: AsyncSession = Depends(get_async_session)):
#     update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    
#     if not update_dict:
#         raise HTTPException(status_code=400, detail="No data provided for update")
    
#     if not update_dict:
#         raise HTTPException(status_code=400, detail="No data provided for update")

#     stmt = (
#         update(student_laboratory)
#         .where(student_laboratory.c.id == student_laboratory_id)
#         .values(**update_dict)
#     )

#     result = await session.execute(stmt)
#     await session.commit()

#     if result.rowcount == 0:
#         raise HTTPException(status_code=404, detail="Discipline not found")

#     return {"status": "success"}

@router.delete("/delete_student_laboratory_by_id")
async def delete_discipline_by_id(student_laboratory_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(student_laboratory).where(student_laboratory.c.id == student_laboratory_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.get("/get_all_student_laboratory")
async def get_all_subject(session: AsyncSession = Depends(get_async_session)):
    query = select(student_laboratory)
    result = await session.execute(query)
    return result.mappings().all()