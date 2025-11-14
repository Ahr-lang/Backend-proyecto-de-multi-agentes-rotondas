FastAPI backend boilerplate for Unity

This is a small boilerplate to use a FastAPI backend from Unity (HTTP or WebGL compatible endpoints).

Features
- /health
- /agents - register/list/update
- /commands - queue commands for Unity agents
- CORS configured to allow calls from Unity (WebGL) or local Unity Editor

Endpoints

- GET /health -> {status: "ok"}
- POST /agents/ -> register {name, type?, meta?} -> returns created agent
- GET /agents/ -> list agents
- GET /agents/{id} -> agent details
- PUT /agents/{id} -> update agent
- POST /commands/enqueue -> enqueue command {agent_id, command, params}
- POST /commands/dequeue?agent_id=ID -> retrieve next command for agent
- GET /commands/list/{agent_id} -> list queued commands

Run locally

# Create a virtualenv (Windows PowerShell)
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run dev server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Docker

Build image: docker build -t unity-fastapi .
Run: docker run -p 8000:8000 unity-fastapi

Unity usage

Use UnityWebRequest for HTTP requests. Example (C#):

using UnityEngine.Networking;
using UnityEngine;

public class Example : MonoBehaviour
{
    IEnumerator Start()
    {
        UnityWebRequest www = UnityWebRequest.Get("http://localhost:8000/health");
        yield return www.SendWebRequest();
        if (www.result == UnityWebRequest.Result.Success)
            Debug.Log(www.downloadHandler.text);
        else
            Debug.LogError(www.error);
    }
}

    Example: register, queue, and dequeue (Unity):

    ```
    using UnityEngine;
    using UnityEngine.Networking;
    using System.Collections;

    public class UnityApiExample : MonoBehaviour
    {
        IEnumerator Start()
        {
            // register
            UnityWebRequest register = UnityWebRequest.Post("http://localhost:8000/agents/", "");
            register.uploadHandler = new UploadHandlerRaw(System.Text.Encoding.UTF8.GetBytes("{\"name\": \"UnityAgent\"}"));
            register.SetRequestHeader("Content-Type", "application/json");
            yield return register.SendWebRequest();

            Debug.Log(register.downloadHandler.text);

            // enqueue command
            UnityWebRequest enqueue = UnityWebRequest.Post("http://localhost:8000/commands/enqueue", "");
            string payload = "{\"agent_id\": \"REPLACE_AGENT_ID\", \"command\": \"move\", \"params\": {\"x\": 1}}";
            enqueue.uploadHandler = new UploadHandlerRaw(System.Text.Encoding.UTF8.GetBytes(payload));
            enqueue.SetRequestHeader("Content-Type", "application/json");
            yield return enqueue.SendWebRequest();
            Debug.Log(enqueue.downloadHandler.text);

            // dequeue
            UnityWebRequest dequeue = UnityWebRequest.Post("http://localhost:8000/commands/dequeue?agent_id=REPLACE_AGENT_ID", "");
            yield return dequeue.SendWebRequest();
            Debug.Log(dequeue.downloadHandler.text);
        }
    }
    ```

Questions or feature ideas: WebSocket support for real-time, auth tokens, persistence to DB.