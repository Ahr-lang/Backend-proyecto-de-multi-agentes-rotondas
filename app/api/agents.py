from fastapi import APIRouter, HTTPException
from app.models.agent import AgentCreate, Agent, AgentUpdate
from uuid import uuid4
from typing import Dict, List

router = APIRouter()

# Very small in-memory storage for demo
agents_store: Dict[str, Agent] = {}

@router.post("/", response_model=Agent)
async def register_agent(payload: AgentCreate):
    """Register a new agent. Unity can use this to identify its session."""
    agent_id = str(uuid4())
    agent = Agent(id=agent_id, **payload.dict())
    agents_store[agent_id] = agent
    return agent

@router.get("/", response_model=List[Agent])
async def list_agents():
    return list(agents_store.values())

@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str):
    if agent_id not in agents_store:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agents_store[agent_id]

@router.put("/{agent_id}", response_model=Agent)
async def update_agent(agent_id: str, payload: AgentUpdate):
    if agent_id not in agents_store:
        raise HTTPException(status_code=404, detail="Agent not found")
    existing = agents_store[agent_id]
    updated = existing.copy(update=payload.dict(exclude_unset=True))
    agents_store[agent_id] = updated
    return updated
