import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contracts.schemas import UserRequest
from orchestrator.graph import aura_graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_item_ids(text: str) -> list:
    pattern = r'\b(?:top|bottom|foot|outer|acc)_\d{3}\b'
    return list(set(re.findall(pattern, text)))

@app.post("/recommend")
async def recommend_outfit(request: UserRequest):
    result = aura_graph.invoke({
        "user_request": request,
        "retry_count": 0
    })
    return {
        "explanation": result["outfit_summary"],
        "fullReasoning": result["outfit_reasoning"],
        "compatibilityScore": result["outfit_score"].score,
        "scoreReasoning": result["outfit_score"].reasoning,
        "itemIds": extract_item_ids(result["outfit_reasoning"]),
    }