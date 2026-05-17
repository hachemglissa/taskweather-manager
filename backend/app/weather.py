import requests

API_KEY = "49f206ba91c4b1e04307f3d858017fd1"

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