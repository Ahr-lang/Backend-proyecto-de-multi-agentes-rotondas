from pydantic import BaseModel
from typing import Optional

class AgentCreate(BaseModel):
    name: str
    type: Optional[str] = None
    meta: Optional[dict] = None

class Agent(AgentCreate):
    id: str

class AgentUpdate(BaseModel):
    name: Optional[str]
    type: Optional[str]
    meta: Optional[dict]
