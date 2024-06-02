from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from auth.schemas import Group

class LaboratoryCreate(BaseModel):
    name: str
    url: str
    discipline_id: int
    deadline: datetime

class LaboratoryUpdate(BaseModel):
    name: str
    url: str
    deadline: datetime

class DisciplineCreate(BaseModel):
    subject_id: int

class DisciplineFullCreate(BaseModel):
    group_id_list: list[int]
    subject_id: int
    teacher_id_list: list[int]

class DisciplineUpdate(BaseModel):
    subject_id: int

class DisciplineUpdate_2(BaseModel):
    id: int
    group_id_list: list[int]
    teacher_id_list: list[int]

# class SubjectRead(BaseModel):
#     id: int
#     name: str
#     class Config:
#         from_attributes = True

class SubjectCreate(BaseModel):
    name: str

class DisciplineGroupCreate(BaseModel):
    group_id: int
    discipline_id: int

class DisciplineResponse(BaseModel):
    discipline_id: int
    subject: str
    groups: list[Group]


class SpecLaboratory(BaseModel):
    laboratory_id: int
    name: str
    deadline: datetime
    status: bool # s
    valid: bool # s
    count_try: int # s
    url_teacher: str
    last_update_date: datetime # s
    url_student: str # s
    reviewers_id: Optional[int] = None # s

class LaboratoryStudentResponse(BaseModel):
    discipline_id: int
    subject: str
    groups: list[Group]
    laboratory_list: list[SpecLaboratory]