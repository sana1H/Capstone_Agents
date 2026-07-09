from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from contracts.schemas import UserRequest, ClothingItem, OutfitScore
from agents.wardrobe_agent import get_wardrobe
from agents.weather_agent import analyze_weather
from agents.occasion_agent import analyze_occasion
from agents.fashion_agent import analyze_fashion_trends
from agents.user_preference_agent import analyze_user_preference
from agents.scoring_agent import score_outfit
from tools.llm_client import call_llm
import json

class AuraState(TypedDict):
    user_request: UserRequest
    wardrobe_items: List[ClothingItem]
    weather_context: str
    occasion_context: str
    fashion_context: str
    user_pref_context: str
    outfit_reasoning: str
    outfit_score: OutfitScore
    retry_count: int
    outfit_summary: str

    #above is the state of a node for our langgraph 

#lets create fisrt node in lang graph 
# In LangGraph, every node is a function that takes 
# the current state and returns a dictionary of 
# updated fields.

def wardrobe_node(state:AuraState) -> dict:
    user_id = state["user_request"].user_id
    wardrobe_items = get_wardrobe(user_id)
    return {"wardrobe_items" : wardrobe_items}

def weather_node(state: AuraState) -> dict:
    city = state["user_request"].city
    weather_context = analyze_weather(city)
    return {"weather_context": weather_context}


def occasion_node(state: AuraState) -> dict:
    request = state["user_request"]
    occasion_context = analyze_occasion(
        request.occasion,
        request.mood,
    )
    return {"occasion_context": occasion_context}


def fashion_node(state: AuraState) -> dict:
    request = state["user_request"]
    fashion_context = analyze_fashion_trends(
        request.occasion,
        request.mood,
    )
    return {"fashion_context": fashion_context}


def user_pref_node(state: AuraState) -> dict:
    user_id = state["user_request"].user_id
    user_pref_context = analyze_user_preference(user_id)
    return {"user_pref_context": user_pref_context}

# now outfit generation , all teh input from above nodes goes to another node called outfit_generator

def outfit_generator_node(state: AuraState) -> dict:
    wardrobe_text = "\n".join([
        (
            f"- ID: {item.cloth_id}\n"
            f"  Category: {item.category} | Subcategory: {item.subcategory}\n"
            f"  Color: {item.color_name} | Fabric: {item.fabric} | Fit: {item.fit}\n"
            f"  Seasons: {', '.join(item.season)}\n"
            f"  Style Tags: {', '.join(item.style_tags)}\n"
            f"  Occasion Tags: {', '.join(item.occasion_tags)}"
        )
        for item in state["wardrobe_items"]
    ])

    json_format = '{\n    "outfit_summary": "3-4 sentence summary for the user.",\n    "outfit_reasoning": "Detailed item-by-item justification for the scoring agent."\n}'

    prompt = (
        "You are an expert AI fashion stylist.\n"
        "Your task is to recommend the BEST outfit using ONLY the wardrobe items listed below.\n\n"
        "========================\n"
        "AVAILABLE WARDROBE\n"
        "========================\n"
        + wardrobe_text +
        "\n\n========================\n"
        "WEATHER CONTEXT\n"
        "========================\n"
        + state["weather_context"] +
        "\n\n========================\n"
        "OCCASION CONTEXT\n"
        "========================\n"
        + state["occasion_context"] +
        "\n\n========================\n"
        "FASHION TREND CONTEXT\n"
        "========================\n"
        + state["fashion_context"] +
        "\n\n========================\n"
        "USER PREFERENCE CONTEXT\n"
        "========================\n"
        + state["user_pref_context"] +
        "\n\nInstructions:\n"
        "1. ONLY use clothing items from the wardrobe above.\n"
        "2. Select a complete outfit (top, bottom, footwear, optional outerwear and accessory).\n"
        "3. Reference items by their ID.\n"
        "4. Justify each item using weather, occasion, user preferences, and fashion trends.\n"
        "5. Never invent clothing items that do not exist in the wardrobe.\n\n"
        "Return ONLY valid JSON in exactly this format:\n\n"
        + json_format +
        "\n\nRules:\n"
        "- Return ONLY valid JSON.\n"
        "- Do NOT include markdown.\n"
        "- Do NOT wrap in ```json.\n"
        "- Do NOT add any extra text.\n"
        "- The JSON must be directly parsable using json.loads().\n"
        """- "outfit_summary" must be a plain string, NOT a JSON object or nested structure.
- "outfit_reasoning" must be a plain string, NOT a JSON object or nested structure.
- Example of correct outfit_summary: "A navy polo paired with beige chinos and formal shoes creates a smart professional look perfect for a work setting."""
    )

    response = call_llm(prompt)
    response = response.strip()

    if response.startswith("```"):
        response = response.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(response)
        return {
            "outfit_reasoning": data["outfit_reasoning"],
            "outfit_summary": data["outfit_summary"],
        }
    except Exception as e:
        raise ValueError(
            f"Failed to parse outfit JSON.\nLLM Response:\n{response}"
        ) from e


def scoring_node(state: AuraState) -> dict:
    outfit_score = score_outfit(
        outfit_reasoning=state["outfit_reasoning"],
        weather_context=state["weather_context"],
        occasion_context=state["occasion_context"],
        user_pref_context=state["user_pref_context"],
        fashion_context=state["fashion_context"],
    )
    return {"outfit_score": outfit_score}


def should_retry(state: AuraState) -> str:
    score = state["outfit_score"].score
    retry_count = state.get("retry_count", 0)

    if score >= 80 or retry_count >= 3:
        return "accept"
    return "retry"


def increment_retry(state: AuraState) -> dict:
    return {"retry_count": state.get("retry_count", 0) + 1}


# ── Build the graph ──────────────────────────────────────────────
def build_graph():
    graph = StateGraph(AuraState)

    # Add all nodes
    graph.add_node("wardrobe", wardrobe_node)
    graph.add_node("weather", weather_node)
    graph.add_node("occasion", occasion_node)
    graph.add_node("fashion", fashion_node)
    graph.add_node("user_pref", user_pref_node)
    graph.add_node("outfit_generator", outfit_generator_node)
    graph.add_node("scoring", scoring_node)
    graph.add_node("increment_retry", increment_retry)

    # Wave 1 — parallel agents from START
    graph.set_entry_point("wardrobe")
    graph.add_edge("wardrobe", "weather")
    graph.add_edge("weather", "occasion")
    graph.add_edge("occasion", "fashion")
    graph.add_edge("fashion", "user_pref")
    graph.add_edge("user_pref", "outfit_generator")
    graph.add_edge("outfit_generator", "scoring")

    # Conditional retry logic
    graph.add_conditional_edges(
        "scoring",
        should_retry,
        {
            "accept": END,
            "retry": "increment_retry",
        }
    )
    graph.add_edge("increment_retry", "outfit_generator")

    return graph.compile()


aura_graph = build_graph()




#test
if __name__ == "__main__":
    from contracts.schemas import UserRequest

    request = UserRequest(
        user_id="user_001",
        mood="Confident",
        occasion="Party",
        city="Delhi"
    )

    result = aura_graph.invoke({
        "user_request": request,
        "retry_count": 0
    })

    print("\n===== OUTFIT RECOMMENDATION =====")
    print(result["outfit_reasoning"])
    print("\n===== OUTFIT SCORE =====")
    print(result["outfit_score"])