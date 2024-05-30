from datetime import datetime
from pydantic import BaseModel

class StudentLaboratoryCreate(BaseModel):
    id_lab: int
    name: str
    url: str
    
class StudentLaboratoryUpdate(BaseModel):
    name: str
    url: str