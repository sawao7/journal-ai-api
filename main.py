import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


class JournalEntry(BaseModel):
    date: int
    journal: str


class JournalInput(BaseModel):
    journal: str
    role: str
    goal: str


@app.post("/update_progress")
async def create_journal(input_data: JournalInput):
    journal_entry = input_data.inputs
    print(journal_entry)
    return {"output": "updated progress"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
