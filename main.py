# {
#     "inputs": {
#         "role": "string",
#         "journal": "string",
#         "goal": "string",
#         "progress": "string",
#     }
# }

# {"output":"string"}

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


class JournalEntry(BaseModel):
    role: str
    journal: str
    goal: str
    progress: str


class JournalInput(BaseModel):
    inputs: JournalEntry


@app.post("/journal")
async def create_journal(input_data: JournalInput):
    journal_entry = input_data.inputs
    print(journal_entry)
    return {"output": "updated progress"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
