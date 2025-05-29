from pydantic import BaseModel
from datetime import datetime

class PostGoal(BaseModel):
    title: str
    description: str

class GetGoal(BaseModel):
    id: int
    title: str
    description: str
    owner_nick: str
    created_at: datetime
    
class PostTask(BaseModel):
    title: str
    description: str
    
class GetTask(BaseModel):
    id: int
    title: str
    description: str
    owner_nick: str
    created_at: datetime
    status: str
    files: list[str]