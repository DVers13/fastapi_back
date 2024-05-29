from datetime import datetime

from pydantic import BaseModel


class LaboratoryCreate(BaseModel):
    name: str
    description: str
    discipline_id: int
    deadline: datetime

class LaboratoryUpdate(BaseModel):
    name: str
    description: str
    discipline_id: int
    deadline: datetime

class DisciplineCreate(BaseModel):
    info: str
    subject_id: int

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