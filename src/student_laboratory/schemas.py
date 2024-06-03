from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class StudentLaboratoryCreate(BaseModel):
    id_lab: int
    id_teacher: Optional[int] = None
    id_discipline: int
    url: str
    
class StudentLaboratoryUpdate(BaseModel):
    student_laboratory_id: int
    id_teacher: Optional[int] = None
    url: str

class StudentInfo(BaseModel):
    id: int
    name: str
    group: str

class DisciplineInfo(BaseModel):
    id: int
    name: str
class StudentLaboratoryGet(BaseModel):
    student_laboratory_id: int
    laboratory_name: str
    student: StudentInfo
    discipline: DisciplineInfo
    deadline: datetime
    loading_time: datetime
    url_task: str
    url_student_task: str
    status: bool
    valid: bool
    count_try: int