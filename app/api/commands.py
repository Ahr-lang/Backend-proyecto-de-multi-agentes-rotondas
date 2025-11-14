from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List

router = APIRouter()

class CommandRequest(BaseModel):
    agent_id: str
    command: str
    params: Optional[dict] = None

# simple FIFO command queue by agent id
commands_queue: Dict[str, List[CommandRequest]] = {}

@router.post("/enqueue", status_code=201)
async def enqueue(cmd: CommandRequest):
    if cmd.agent_id not in commands_queue:
        commands_queue[cmd.agent_id] = []
    commands_queue[cmd.agent_id].append(cmd)
    return {"status": "queued"}

@router.post("/dequeue")
async def dequeue(agent_id: str):
    """Unity calls this to pull the next command for an agent. Returns 404 when none are available."""
    if agent_id not in commands_queue or len(commands_queue[agent_id]) == 0:
        raise HTTPException(status_code=404, detail="No commands queued")
    return commands_queue[agent_id].pop(0)

@router.get("/list/{agent_id}")
async def list_commands(agent_id: str):
    return commands_queue.get(agent_id, [])
