from datetime import datetime

from pydantic import BaseModel


class LaboratoryCreate(BaseModel):
    id: int
    name: str
    description: str
    discipline_id: int
    date: datetime

class DisciplineCreate(BaseModel):
    id: int
    info: str
    subject_id: int