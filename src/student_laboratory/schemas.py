from datetime import datetime
from pydantic import BaseModel

class StudentLaboratoryCreate(BaseModel):
    name: str
    url: str
    