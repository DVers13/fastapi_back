from datetime import datetime

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
    discipline_id: int
    deadline: datetime

class DisciplineCreate(BaseModel):
    info: str
    subject_id: int

class DisciplineFullCreate(BaseModel):
    group_id_list: list[int]
    subject_id: int
    info: str
    teacher_id_list: list[int]

class DisciplineUpdate(BaseModel):
    info: str
    subject_id: int

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