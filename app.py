import string

from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
from backend.core import run_llm, run_llm2
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust for your security needs
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],
)


class Query(BaseModel):
    query: str
    chat_history: List[Dict]


@app.post("/get_order_details/")
def get_order_details(order_id: str):
    order_id = order_id.strip()
    if len(order_id) != 7:
        ids = order_id.split("=")
        if len(ids) == 2:
            order_id = ids[1].strip()
            order_id = remove_special_chars(order_id)

    url = f"https://api.a4b.io/gw1/puja/external/v1/bookings/{order_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=400, detail=f"HTTP error: {http_err}")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")


def remove_special_chars(s: str) -> str:
    """Remove trailing special characters."""
    return s.strip(string.punctuation)


@app.post("/chat")
def chat(query: Query):
    # Call the run_llm function with query and chat history
    result = run_llm(query.query, query.chat_history)

    # Return the updated chat history along with the new AI response
    updated_chat_history = query.chat_history + [{"role": "ai", "content": result['answer']}]
    return {"result": {"answer": result['answer'], "chat_history": updated_chat_history}}


# Input model for the API
class LLMInput(BaseModel):
    query: str
    chat_history: List[Dict[str, Any]] = []


# Endpoint for run_llm
@app.post("/run_llm/")
async def run_llm_endpoint(input_data: LLMInput):
    try:
        result = run_llm(input_data.query, input_data.chat_history)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint for run_llm2
@app.post("/run_llm2/")
async def run_llm2_endpoint(input_data: LLMInput):
    try:
        result = run_llm2(input_data.query, input_data.chat_history)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run: uvicorn app:app --reload
