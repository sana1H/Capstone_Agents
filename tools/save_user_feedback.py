import json
from datetime import datetime
from pathlib import Path

from contracts.schemas import OutfitScore


FEEDBACK_PATH = (
    Path(__file__).parent.parent
    / "mock_data"
    / "feedback.json"
)


def save_user_feedback(
    user_id: str,
    outfit_reasoning: str,
    outfit_score: OutfitScore,
) -> None:
    """
    Persist user feedback for future personalization.
    """

    if FEEDBACK_PATH.exists():
        with open(FEEDBACK_PATH, "r", encoding="utf-8") as f:
            feedback = json.load(f)
    else:
        feedback = []

    feedback.append(
        {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "outfit_reasoning": outfit_reasoning,
            "score": outfit_score.score,
            "reasoning": outfit_score.reasoning,
        }
    )

    with open(FEEDBACK_PATH, "w", encoding="utf-8") as f:
        json.dump(feedback, f, indent=4)