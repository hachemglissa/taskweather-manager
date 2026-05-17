import requests

API_KEY = "d2603c6572d6d305b46ff02dbf1c3469"

def get_weather(city: str):

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    data = response.json()

    print("API RESPONSE:", data)

    # gestion erreur propre
    if response.status_code != 200 or "main" not in data:
        return {
            "temp": "N/A",
            "condition": data.get("message", "API Error")
        }

    return {
        "temp": data["main"]["temp"],
        "condition": data["weather"][0]["main"]
    }