from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class StudentLaboratoryCreate(BaseModel):
    id_lab: int
    id_student: int
    id_teacher: Optional[int] = None
    id_discipline: int
    url: str
    
class StudentLaboratoryUpdate(BaseModel):
    student_laboratory_id: int
    url: str