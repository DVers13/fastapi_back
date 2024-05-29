from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from student_laboratory.models import student_laboratory
# from student_laboratory.schemas import SLaboratoryCreate

router = APIRouter(
    prefix="/student_laboratory",
    tags=["student_laboratory"]
)

@router.get("/")
async def get_student_laboratory_by_id(student_laboratory_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(student_laboratory).where(student_laboratory.c.id == student_laboratory_id)
    result = await session.execute(query)
    return result.all()


