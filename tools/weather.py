import requests
from langchain_core.tools import tool

from settings import DEFAULT_CITY

CODES = {
    0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "fog", 48: "fog", 51: "light drizzle", 53: "drizzle", 55: "heavy drizzle",
    61: "light rain", 63: "rain", 65: "heavy rain", 71: "light snow", 73: "snow",
    75: "heavy snow", 80: "rain showers", 81: "rain showers", 82: "violent rain showers",
    95: "thunderstorm", 96: "thunderstorm with hail", 99: "thunderstorm with hail",
}


@tool
def get_weather(city: str = "") -> str:
    """Get the current weather and today's high and low for a city. Pass the city name the user gave."""
    city = city.strip() or DEFAULT_CITY
    if not city:
        return "No city given. Ask the user which city."
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "format": "json"}, timeout=10,
        ).json()
        if not geo.get("results"):
            return f"Could not find a city called {city}."
        place = geo["results"][0]
        data = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": place["latitude"], "longitude": place["longitude"],
                "current": "temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
                "forecast_days": 1, "timezone": "auto",
            }, timeout=10,
        ).json()
        cur, day = data["current"], data["daily"]
        return (
            f"{place['name']}, {place.get('country', '')}: "
            f"{CODES.get(cur['weather_code'], 'unknown conditions')}, "
            f"{cur['temperature_2m']}°C (feels {cur['apparent_temperature']}°C), "
            f"humidity {cur['relative_humidity_2m']}%, wind {cur['wind_speed_10m']} km/h. "
            f"Today: high {day['temperature_2m_max'][0]}°C, low {day['temperature_2m_min'][0]}°C, "
            f"rain chance {day['precipitation_probability_max'][0]}%."
        )
    except Exception as e:
        return f"Weather error: {e}"


WEATHER_TOOLS = [get_weather]