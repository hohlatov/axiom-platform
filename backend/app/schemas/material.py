from pydantic import BaseModel
from typing import Optional

class MaterialBase(BaseModel):
    title: str
    content: str
    grade: Optional[str] = None
    subject: Optional[str] = None
    
class MaterialCreate(MaterialBase):
    pass

class MaterialResponse(MaterialBase):
    id: int
    owner_id: int
    
    class Config:
        from_attributes = True