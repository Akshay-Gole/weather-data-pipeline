import requests
import json

URL = "https://api.open-meteo.com/v1/forecast?latitude=-34.93&longitude=138.60&hourly=temperature_2m,relative_humidity_2m&forecast_days=3&timezone=Australia%2FAdelaide"

def convert_to_records(data):
    hourly_data = data["hourly"]
    times = hourly_data["time"]
    temperatures = hourly_data["temperature_2m"]
    humidities = hourly_data["relative_humidity_2m"]

    if not (len(times) == len(temperatures) == len(humidities)):
        raise ValueError(
            f"Hourly list lengths differ: "
            f"time={len(times)}, "
            f"temperature={len(temperatures)}, "
            f"humidity={len(humidities)}"
        )

    hourly_extracted_records = []

    for i in range(len(times)):
        hourly_extracted_records.append({"timestamp": times[i], "temperature_c": temperatures[i], "humidity_pct": humidities[i]})

    return hourly_extracted_records


try:
    response = requests.get(URL, timeout=(5, 15))
    response.raise_for_status()

    data = response.json()

    with open("raw_weather.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    records = convert_to_records(data)
    print(f"Number of records: {len(records)}")
    print(records[:2])



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
except ValueError as error:
    print(f"Could not convert weather data: {error}")
