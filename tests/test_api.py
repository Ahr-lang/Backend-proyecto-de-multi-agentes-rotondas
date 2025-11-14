import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_agents_register_and_list():
    r = client.post("/agents/", json={"name": "Agent Unity"})
    assert r.status_code == 200
    data = r.json()
    assert "id" in data
    agent_id = data["id"]

    list_resp = client.get("/agents/")
    assert list_resp.status_code == 200
    ids = [a["id"] for a in list_resp.json()]
    assert agent_id in ids


def test_commands_enqueue_dequeue():
    # create agent
    r = client.post("/agents/", json={"name": "Cmd Agent"})
    agent_id = r.json()["id"]

    # enqueue
    eq = client.post("/commands/enqueue", json={"agent_id": agent_id, "command": "move", "params": {"x":1}})
    assert eq.status_code == 201

    # list
    list_r = client.get(f"/commands/list/{agent_id}")
    assert list_r.status_code == 200
    assert len(list_r.json()) == 1

    # dequeue
    dq = client.post("/commands/dequeue", params={"agent_id": agent_id})
    assert dq.status_code == 200
    assert dq.json()["command"] == "move"

    # now empty
    empty = client.post("/commands/dequeue", params={"agent_id": agent_id})
    assert empty.status_code == 404
