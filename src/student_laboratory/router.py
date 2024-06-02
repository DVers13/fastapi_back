from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, delete, select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from auth.models import User, user
from laboratory.models import discipline_teacher, laboratory, subject, discipline
from student_laboratory.models import student_laboratory
from student_laboratory.schemas import DisciplineInfo, StudentInfo, StudentLaboratoryCreate, StudentLaboratoryForTeacher, StudentLaboratoryUpdate
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
async def get_student_laboratory_for_teacher(user_tg: User = Depends(current_user),
                                        session: AsyncSession = Depends(get_async_session),
                                        is_personally: bool = Query(False),
                                        discipline_id: int = Query(None),
                                        group_id: int = Query(None)) -> list[StudentLaboratoryForTeacher]:
    teacher_id = user_tg.id
    labs_without_teacher = []

    filters = [student_laboratory.c.status == False, student_laboratory.c.valid == True]
    if discipline_id is not None:
        filters.append(student_laboratory.c.id_discipline == discipline_id)
    if group_id is not None:
        filters.append(user.c.group_id == group_id)

    query_with_teacher = select(student_laboratory).join(laboratory, laboratory.c.id == student_laboratory.c.id_lab).join(user, user.c.id == student_laboratory.c.id_student).where(student_laboratory.c.id_teacher == teacher_id)
    
    if not is_personally:
        query_without_teacher = select(student_laboratory).join(laboratory, laboratory.c.id == student_laboratory.c.id_lab).join(user, user.c.id == student_laboratory.c.id_student).where(student_laboratory.c.id_teacher.is_(None))
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
    finish_laboratory = []
    for lab in sorted_labs:

        query = select(user.c.username).where(user.c.id == lab.id_student)
        result_query = await session.execute(query)
        username = result_query.mappings().first()
        student = StudentInfo(id = lab.id_student, name = username.username)

        query = (select(subject.c.name)
                 .join(discipline, discipline.c.subject_id == subject.c.id)
                 .where(discipline.c.id == lab.id_discipline))
        result_query = await session.execute(query)
        subjectname = result_query.mappings().first()
        discipline_info = DisciplineInfo(id = lab.id_discipline, name = subjectname.name)

        query = (select(laboratory.c.url, laboratory.c.deadline)
                 .where(laboratory.c.id == lab.id_lab))
        result_query = await session.execute(query)
        laboratory_info = result_query.mappings().first()
        deadline = laboratory_info.deadline
        url_task = laboratory_info.url
        laboratory_teach = StudentLaboratoryForTeacher(student_laboratory_id = lab.id,
                                                        student = student,
                                                        discipline = discipline_info,
                                                        deadline = deadline,
                                                        loading_time = lab.loading_time,
                                                        url_task = url_task,
                                                        url_student_task = lab.url,
                                                        status = lab.status,
                                                        valid = lab.valid,
                                                        count_try = lab.count_try)
        finish_laboratory.append(laboratory_teach)
    return finish_laboratory

@router.post("/add_student_laboratory")
async def add_student_laboratory(new_student_laboratory: Annotated[StudentLaboratoryCreate, Depends()], user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    
    query = (select(student_laboratory.c.id_lab).where(student_laboratory.c.id_student == user.id))
    result = await session.execute(query)
    result_dict = result.mappings().all()
    print(result_dict)
    id_labs_valid = [lab.id_lab for lab in result_dict]

    if new_student_laboratory.id_lab in id_labs_valid:
        raise HTTPException(status_code=404, detail="Student laboratory already created")
    
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

@router.patch("/accept_student_laboratory/", dependencies=[Depends(check_permissions(["accept"]))])
async def accept_student_laboratory(student_laboratory_id: int, session: AsyncSession = Depends(get_async_session)):
    
    stmt = (
        update(student_laboratory)
        .where(student_laboratory.c.id == student_laboratory_id)
        .values(status = True)
    )

    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student laboratory not found")

    return {"status": "success"}


@router.patch("/deny_student_laboratory/", dependencies=[Depends(check_permissions(["deny"]))])
async def deny_student_laboratory(student_laboratory_id: int, session: AsyncSession = Depends(get_async_session)):
    
    stmt = (
        update(student_laboratory)
        .where(student_laboratory.c.id == student_laboratory_id)
        .values(valid = False)
    )

    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student laboratory not found")

    return {"status": "success"}

@router.patch("/repeat_student_laboratory/", dependencies=[Depends(check_permissions(["update"]))])
async def repeat_student_laboratory(update_data: Annotated[StudentLaboratoryUpdate, Depends()], session: AsyncSession = Depends(get_async_session)):
    stmt = (
        update(student_laboratory)
        .where(student_laboratory.c.id == update_data.student_laboratory_id)
        .values(url = update_data.url,
                count_try=student_laboratory.c.count_try + 1,
                valid = True)
    )

    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student laboratory not found")

    return {"status": "success"}

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