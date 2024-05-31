from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from auth.models import User
from student_laboratory.models import student_laboratory
from student_laboratory.schemas import StudentLaboratoryCreate, StudentLaboratoryUpdate
from auth.base_config import current_user
router = APIRouter(
    prefix="/student_laboratory",
    tags=["student_laboratory"]
)

@router.get("/get_student_laboratory_by_id")
async def get_student_laboratory_by_id(student_laboratory_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(student_laboratory).where(student_laboratory.c.id == student_laboratory_id)
    result = await session.execute(query)
    return result.all()

@router.post("/add_student_laboratory")
async def add_student_laboratory(new_student_laboratory: Annotated[StudentLaboratoryCreate, Depends()], user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    new_student_laboratory_dict = new_student_laboratory.model_dump()
    new_student_laboratory_dict["id_student"] = user.id
    new_student_laboratory_dict["status"] = False
    new_student_laboratory_dict["score"] = "0"
    new_student_laboratory_dict["count_try"] = 0
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