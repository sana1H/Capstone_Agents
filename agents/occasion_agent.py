# same as fashion, take user input and call LLM , returns resoning 
# heres its all maojroly a prompt and a call to llm_client.py
from tools.llm_client import call_llm


def analyze_occasion(occasion: str, mood: str) -> str:
    """
    Analyze the occasion and mood to generate styling constraints
    for the outfit recommendation system.
    """

    prompt = f"""
You are an expert fashion consultant.

Your task is NOT to recommend a complete outfit.

Instead, generate occasion-aware styling guidance that will be consumed
by another AI responsible for selecting clothes from a user's wardrobe.

Occasion:
{occasion}

Mood:
{mood}

Analyze the occasion and infer:

1. Expected level of formality.
2. Appropriate dress code.
3. Suitable overall aesthetic.
4. Preferred clothing structure (relaxed, tailored, oversized, fitted, etc.).
5. Suitable color palette.
6. Accessories that are generally appropriate.
7. Footwear style expectations.
8. Items or styles that should generally be avoided.
9. Any special social or cultural expectations relevant to this occasion.

Important:
- Provide guidance only.
- Do NOT recommend specific garments.
- Assume the wardrobe already exists.
- Keep the response concise (150-200 words).
- Write in natural language so another AI can use this reasoning while selecting an outfit.
"""

    return call_llm(prompt)


# if __name__ == "__main__":
#     result = analyze_occasion("Party", "Confident")
#     print(result)


# (150-200 words) as a constraint in your prompt. That's good prompt engineering instinct. Controlling output length prevents the LLM from rambling, which matters when this gets bundled with 4 other agent outputs into one orchestrator prompt
