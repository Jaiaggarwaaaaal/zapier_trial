from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks = []
API_KEYS = {"test-key-123": True}

class TaskRequest(BaseModel):
    task: str

@app.get("/api/tasks")
async def get_tasks(x_api_key: str = Header(...)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return tasks[-5:]

@app.post("/api/add-task")
async def add_task(request: TaskRequest, x_api_key: str = Header(...)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    task_entry = {"id": len(tasks) + 1, "task": request.task, "time": datetime.now().isoformat()}
    tasks.append(task_entry)
    return {"message": f"Task '{request.task}' added with ID {task_entry['id']}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)