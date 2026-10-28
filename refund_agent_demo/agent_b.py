import json
import ollama
from fastapi import FastAPI

app = FastAPI()

SYSTEM = """You are a billing agent. You receive refund requests from another agent.
Approve refunds of only $100 or less, only if they include a plausible reason. Deny anything that doesn't fulfill either criteria.
Respond with ONLY a JSON object:
{"decision":"approve" or "deny", "reason":"<one short sentence>"}"""

@app.post("/refund")
def refund(body: dict):

    print(f"[B] received request: {body}")
    resp=ollama.chat(
            model="llama3.2",
            format="json",
            messages=[
                {"role":"system", "content":SYSTEM},
                {"role":"user", "content":json.dumps(body)},])
    try:
        decision=json.loads(resp.message.content)
    except json.JSONDecodeError:
        decision={"decision":"deny","reason":"could not parse model output"}
    print(f"[B] decision:{decision}")
    return decision
