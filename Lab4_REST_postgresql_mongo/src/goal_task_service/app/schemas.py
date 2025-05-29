from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class GoalCreate(BaseModel):
    title: str
    text: str
    owner_nick: str


class GoalRead(BaseModel):
    id: int
    title: str
    text: str
    owner_nick: str
    created_at: datetime
    
    model_config = {
        "from_attributes": True,
        "orm_mode": True,
    }


class TaskCreate(BaseModel):
    title: str
    text: str
    owner_nick: str
    files: Optional[Dict[str, str]] = None
    goal_id: Optional[int] = None


class TaskRead(BaseModel):
    id: int
    title: str
    text: str
    owner_nick: str
    files: Optional[Dict[str, str]] = None
    created_at: datetime
    goal_id: Optional[int]

    model_config = {
        "from_attributes": True,
        "orm_mode": True,
    }

