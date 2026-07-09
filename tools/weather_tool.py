import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

import requests

from contracts.schemas import WeatherContext

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city: str) -> WeatherContext:
    """
    Fetch current weather for a city and return it as a WeatherContext.
    """

    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY is not set.")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",   # Celsius
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    # Determine season from the current month
    month = datetime.now().month
    if month in (3, 4, 5):
        season = "Spring"
    elif month in (6, 7, 8):
        season = "Summer"
    elif month in (9, 10, 11):
        season = "Autumn"
    else:
        season = "Winter"

    return WeatherContext(
        city=data["name"],
        temperature=data["main"]["temp"],
        condition=data["weather"][0]["main"],
        season=season,
    )



#check if this works fine 
if __name__ == "__main__":
    weather = get_weather("Delhi")
    print(weather)

