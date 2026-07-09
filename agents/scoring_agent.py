# its diff form all other agents 
# every other agent is a context provider - it gathers info and return reasoning
# scoring agent is an evaluator



import json

from contracts.schemas import OutfitScore
from tools.llm_client import call_llm


def score_outfit(
    outfit_reasoning: str,
    weather_context: str,
    occasion_context: str,
    user_pref_context: str,
    fashion_context: str,
) -> OutfitScore:
    """
    Evaluate the generated outfit against all available contexts.
    Returns an OutfitScore object.
    """

    prompt = f"""
You are an expert fashion evaluator.

Your job is to evaluate how well the proposed outfit satisfies ALL available contexts.

Weather Context:
{weather_context}

Occasion Context:
{occasion_context}

User Preference Context:
{user_pref_context}

Fashion Trend Context:
{fashion_context}

Generated Outfit:
{outfit_reasoning}

Evaluate the outfit on:

1. Weather suitability
2. Occasion appropriateness
3. Alignment with user preferences
4. Fashion relevance
5. Overall cohesiveness

Give a score from 0-100.

Return ONLY valid JSON.

Required format:

{{
    "score": 87,
    "reasoning": "Explain why this outfit received this score in 3-6 concise sentences."
}}

Do not include markdown.
Do not include ```json.
Do not include any additional text.
"""

    response = call_llm(prompt)

    try:
        data = json.loads(response)
        return OutfitScore(**data)

    except Exception as e:
        raise ValueError(
            f"Unable to parse OutfitScore from LLM response.\n"
            f"Response:\n{response}"
        ) from e

#test    
# if __name__ == "__main__":
#     result = score_outfit( outfit_reasoning="White formal shirt, black slim trousers, black formal shoes, silver watch.",
#         weather_context="Temperature: 21°C, Condition: Clouds, Season: Summer. Prefer cotton, half or full sleeves, optional light jacket.",
#         occasion_context="Smart casual to cocktail. Polished silhouettes, jewel tones or neutrals. Avoid sportswear.",
#         user_pref_context="Minimal, modern aesthetic. Preferred colors: Black, White, Navy. Avoid streetwear and flashy items.",
#         fashion_context="Structured tailoring, jewel tones, metallics trending. Avoid overly casual fabrics.")
#     print(result)