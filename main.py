import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


class JournalEntry(BaseModel):
    date: int
    journal: str


class JournalInput(BaseModel):
    journal: JournalEntry
    role: str
    goal: str

def open_ai_call(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content



@app.post("/update_progress")
async def create_journal(input_data: JournalInput):
    journal_entry = input_data.journal
    journal = journal_entry.journal
    role = input_data.role
    goal = input_data.goal
    # print(journal_entry, role, goal)

    prompt_to_decide_updating_the_progress = f"Determine if the journal entry touches on anything related to the user's goal, whether positively, negatively, or neutrally. Produce a boolean value (true/false) with no extra text, formatting or syntax. JUST RESPOND IN ONE WORD!"
    prompt_to_update_progress = f"Our app is a journaling app where we want to have deep understanding of the user and help users achieve his/her goals. We want to track user’s progress based on each of the goals weekly and give suggestions based on their daily journal entries. Below is one of the user's goals and his daily journal for today. Produce a simple progress excerpt in pure text simply describing what the user did regarding making progress towards the goal for this day. Give no suggestions. No extra formatting and syntax."

    progress_check_prompt = prompt_to_decide_updating_the_progress + \
        f"\nGoal: {goal}\nJournal: {journal}"
    should_update = open_ai_call(progress_check_prompt).lower() == "true"

    if should_update:
        prompt = (prompt_to_update_progress +
                  f"\nGoal: {goal}\n"
                  f"Journal: {journal}")

        response = open_ai_call(prompt)
        print(f"New progress: {response}")
    else:
        response = "No progress"

    return {"output": response}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
