from fastapi import FastAPI
from debate_manager import run_debate

app = FastAPI()

@app.get("/debate")
def debate(topic: str):
    result = run_debate(topic)
    return result