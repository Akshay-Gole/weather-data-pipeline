import requests
import json

URL = "https://api.open-meteo.com/v1/forecast?latitude=-34.93&longitude=138.60&hourly=temperature_2m,relative_humidity_2m&forecast_days=3&timezone=Australia%2FAdelaide"

try:
    response = requests.get(URL, timeout=(5, 15))
    response.raise_for_status()

    data = response.json()

    with open("raw_weather.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

except requests.exceptions.HTTPError as error:
    print(f"HTTP request failed: {error.response.status_code}")
except requests.exceptions.ConnectTimeout:
    print("Connecting to the server took too long.")
except requests.exceptions.ReadTimeout:
    print("Connected, but waiting for data took too long.")
except requests.exceptions.ConnectionError:
    print("The connection failed or broke.")
except requests.exceptions.JSONDecodeError:
    print("The JSON response was not valid.")
except OSError as error:
    print(f"Could not save the weather data: {error}")
