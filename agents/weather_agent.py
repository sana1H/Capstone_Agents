#Agent translates raw data from weather_tool.py into actionable outfit guidance 

from tools.weather_tool import get_weather


def analyze_weather(city: str) -> str:
    """
    Produce structured weather reasoning for the outfit recommendation LLM.
    """

    weather = get_weather(city)

    temperature = weather.temperature
    condition = weather.condition.lower()

    # Temperature reasoning
    if temperature >= 35:
        thermal = "Very Hot"
        preferred_fabrics = "Linen, cotton, moisture-wicking fabrics"
        preferred_sleeves = "Sleeveless or short sleeves"
        layering = "No layering"
        avoid = "Wool, fleece, thick denim, heavy jackets"

    elif temperature >= 28:
        thermal = "Hot"
        preferred_fabrics = "Cotton, linen, lightweight blends"
        preferred_sleeves = "Short sleeves"
        layering = "Minimal layering"
        avoid = "Heavy sweaters, thick outerwear"

    elif temperature >= 20:
        thermal = "Warm"
        preferred_fabrics = "Cotton, light denim, breathable blends"
        preferred_sleeves = "Half or full sleeves"
        layering = "Optional light jacket"
        avoid = "Bulky winter clothing"

    elif temperature >= 12:
        thermal = "Cool"
        preferred_fabrics = "Knits, cotton blends, light wool"
        preferred_sleeves = "Full sleeves"
        layering = "Light sweater or jacket"
        avoid = "Thin summer clothing"

    else:
        thermal = "Cold"
        preferred_fabrics = "Wool, fleece, thermal fabrics"
        preferred_sleeves = "Full sleeves"
        layering = "Multiple insulating layers"
        avoid = "Lightweight summer fabrics"

    # Weather condition reasoning
    weather_notes = []

    if "rain" in condition or "drizzle" in condition:
        weather_notes.append(
            "Prioritize water-resistant outerwear and waterproof footwear."
        )
        weather_notes.append(
            "Avoid fabrics that absorb water easily."
        )

    if "snow" in condition:
        weather_notes.append(
            "Thermal insulation and waterproof outerwear are strongly preferred."
        )

    if "clear" in condition:
        weather_notes.append(
            "No weather-related restrictions."
        )

    if "cloud" in condition:
        weather_notes.append(
            "Light outerwear may improve comfort."
        )

    if any(x in condition for x in ["mist", "fog", "haze"]):
        weather_notes.append(
            "Slight preference for an additional outer layer."
        )

    if "thunder" in condition:
        weather_notes.append(
            "Avoid outfits unsuitable for wet conditions."
        )

    return f"""
WEATHER CONTEXT

City: {weather.city}
Season: {weather.season}
Temperature: {temperature:.1f}°C
Condition: {weather.condition}

Thermal Category:
{thermal}

Preferred Fabrics:
{preferred_fabrics}

Preferred Sleeve Length:
{preferred_sleeves}

Layering Strategy:
{layering}

Avoid:
{avoid}

Additional Weather Constraints:
{" ".join(weather_notes)}

Use these constraints while selecting an outfit. Prioritize clothing that satisfies the thermal requirements first, then weather-specific constraints, while balancing style and user preferences.
""".strip()  #removes and leading or trailing whitespacee and newlines from string

#the above line is prompt engineering decision instructing llm 


#this is just for testing
# if __name__ == "__main__":
#     result = analyze_weather("Delhi")
#     print(result)