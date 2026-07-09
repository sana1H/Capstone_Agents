from contracts.schemas import UserPreference
from tools.llm_client import call_llm


# -------------------------------------------------------------------
# Mock User Database
# Later this can be replaced with a real database.
# -------------------------------------------------------------------

MOCK_USERS = {
    "user_001": UserPreference(
        user_id="user_001",

        preferred_styles=[
            "Minimal",
            "Smart Casual",
            "Modern"
        ],

        disliked_styles=[
            "Streetwear",
            "Bohemian"
        ],

        preferred_colors=[
            "Black",
            "White",
            "Navy",
            "Olive"
        ],

        avoided_colors=[
            "Neon Green",
            "Bright Orange"
        ],

        fit_preference="Regular",

        additional_notes=(
            "I prefer clean and polished outfits that look effortless. "
            "I don't like overly flashy clothing and usually prefer timeless pieces."
        )
    )
}


def analyze_user_preference(user_id: str) -> str:
    """
    Analyze user style preferences and produce reasoning
    for the outfit recommendation system.
    """

    if user_id not in MOCK_USERS:
        raise ValueError(f"Unknown user_id: {user_id}")

    user = MOCK_USERS[user_id]

    prompt = f"""
You are a professional fashion stylist.

Your task is NOT to recommend an outfit.

Instead, analyze the user's long-term fashion preferences and generate
styling constraints that another AI can use while selecting clothes.

User Preferences

Preferred Styles:
{", ".join(user.preferred_styles)}

Disliked Styles:
{", ".join(user.disliked_styles)}

Preferred Colors:
{", ".join(user.preferred_colors)}

Colors to Avoid:
{", ".join(user.avoided_colors)}

Preferred Fit:
{user.fit_preference}

Additional Notes:
{user.additional_notes or "None"}

Generate reasoning covering:

1. Core personal aesthetic.
2. Style principles to prioritize.
3. Color palette preferences.
4. Clothing fits and silhouettes that align with the user.
5. Styles that should generally be avoided.
6. How these preferences should influence outfit selection.

Important:
- Do NOT recommend specific garments.
- Do NOT describe a complete outfit.
- Produce only reasoning that another AI can use.
- Keep the response under 180 words.
"""

    return call_llm(prompt)

#test
# if __name__ == "__main__":
#     result = analyze_user_preference("user_001")
#     print(result)