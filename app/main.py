from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import agents, commands

app = FastAPI(title="Unity FastAPI Backend", version="0.1.0")

# Allow Unity Editor and WebGL; in production change to specific origins
origins = ["http://localhost", "http://localhost:8000", "http://localhost:8001", "*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents.router, prefix="/agents", tags=["agents"]) 
app.include_router(commands.router, prefix="/commands", tags=["commands"]) 


@app.get("/health")
async def health():
    return {"status": "ok"}
