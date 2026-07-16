import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contracts.schemas import UserRequest
from orchestrator.graph import aura_graph
from contracts.schemas import FeedbackRequest
from tools.save_user_feedback import save_user_feedback


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

@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    save_user_feedback(request.user_id, request.outfit_reasoning, request.score_reasoning, request.user_score)
    return {"status": "success", "message": "Feedback saved."}


@app.get("/")
async def root():
    return {
        "name": "AURA API",
        "version": "1.0",
        "docs": "https://web-production-63b634.up.railway.app/docs"
    }