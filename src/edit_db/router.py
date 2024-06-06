import json
from fastapi import APIRouter, Depends
from sqlalchemy import delete, insert, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from auth.models import user, role, group
from laboratory.models import laboratory, discipline, discipline_groups, discipline_teacher, subject
from auth.schemas import GroupCreate, RoleCreate, UserCreate
from student_laboratory.models import student_laboratory
from auth.manager import get_user_manager

router = APIRouter(
    prefix="/edit_db",
    tags=["Edit DataBase"]
)

@router.delete("/clear_all")
async def clear_all(session: AsyncSession = Depends(get_async_session)):
    stmt_role = delete(role)
    await session.execute(stmt_role)

    stmt_user = delete(user)
    await session.execute(stmt_user)

    stmt_group = delete(group)
    await session.execute(stmt_group)

    stmt_laboratory = delete(laboratory)
    await session.execute(stmt_laboratory)

    stmt_discipline = delete(discipline)
    await session.execute(stmt_discipline)

    stmt_discipline_groups = delete(discipline_groups)
    await session.execute(stmt_discipline_groups)

    stmt_discipline_teacher = delete(discipline_teacher)
    await session.execute(stmt_discipline_teacher)

    stmt_subject = delete(subject)
    await session.execute(stmt_subject)

    stmt_student_laboratory = delete(student_laboratory)
    await session.execute(stmt_student_laboratory)

    await session.execute(text("ALTER SEQUENCE user_id_seq RESTART WITH 1"))
    await session.execute(text("ALTER SEQUENCE role_id_seq RESTART WITH 1"))
    await session.execute(text("ALTER SEQUENCE group_id_seq RESTART WITH 1"))
    await session.execute(text("ALTER SEQUENCE subject_id_seq RESTART WITH 1"))
    await session.execute(text("ALTER SEQUENCE discipline_id_seq RESTART WITH 1"))
    await session.execute(text("ALTER SEQUENCE discipline_groups_id_seq RESTART WITH 1"))
    await session.execute(text("ALTER SEQUENCE discipline_teacher_id_seq RESTART WITH 1"))
    await session.execute(text("ALTER SEQUENCE laboratory_id_seq RESTART WITH 1"))
    await session.execute(text("ALTER SEQUENCE student_laboratory_id_seq RESTART WITH 1"))

    await session.commit()
    return {"status": "success"}

@router.post("/fill_data")
async def fill_data(session: AsyncSession = Depends(get_async_session), user_manager = Depends(get_user_manager)):
    sql_files = [
            'edit_db/sql_query/INSERT_INTO_Role.sql',
            'edit_db/sql_query/INSERT_INTO_Group.sql']
    for file_path in sql_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_query = file.read()
        
        await session.execute(text(sql_query))
        await session.commit()

    with open("edit_db/sql_query/CreateUser.txt", 'r', encoding='utf-8') as file:
        user_list = json.load(file)
    for user_data in user_list:
        user_create = UserCreate(**user_data)
        await user_manager.create(user_create)

    dict_update ={"role_id" : 1}
    for user_id in range(11, 19):
        stmt = (
            update(user)
            .where(user.c.id == user_id)
            .values(**dict_update)
        )

        await session.execute(stmt)
        await session.commit()

    sql_files = ['edit_db/sql_query/INSERT_INTO_subject.sql',
                 'edit_db/sql_query/INSERT_INTO_discipline.sql',
                 'edit_db/sql_query/INSERT_INTO_discipline_groups.sql',
                'edit_db/sql_query/INSERT_INTO_discipline_teacher.sql',
                'edit_db/sql_query/INSERT_INTO_laboratory.sql',
                'edit_db/sql_query/INSERT_INTO_student_laboratory.sql',
                ]
    for file_path in sql_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_query = file.read()
        
        await session.execute(text(sql_query))
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

@router.get("/get_all_users")
async def get_all_teachers(session: AsyncSession = Depends(get_async_session)):
    query = select(user)
    result = await session.execute(query)
    return result.mappings().all()

@router.patch("/update_role/")
async def update_role(user_id: int, role_id: int, session: AsyncSession = Depends(get_async_session)):
    dict_update ={"role_id" : role_id}
    stmt = (
        update(user)
        .where(user.c.id == user_id)
        .values(**dict_update)
    )

    await session.execute(stmt)
    await session.commit()

    return {"status": "success"}