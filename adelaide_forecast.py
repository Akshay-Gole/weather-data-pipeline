from datetime import datetime
import requests
import json
import csv

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

def is_valid_timestamp(ts):
    try:
        datetime.strptime(ts, "%Y-%m-%dT%H:%M")
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def is_valid_temperature(temp):
    if temp is None:
        return False

    if not isinstance(temp, (int, float)) or isinstance(temp, bool):
        return False

    return True

def is_valid_humidity(hum):
    if hum is None:
        return False

    if not isinstance(hum, (int, float)):
        return False

    if hum < 0 or hum > 100:
        return False

    return True

def clean_records(records):
    kept_records = []
    rejected_records = []
    duplicate_records = []
    timestamps = set()

    for i in records:
        ts = i.get("timestamp")
        temperature = i.get("temperature_c")
        humidity = i.get("humidity_pct")

        if is_valid_timestamp(ts) and is_valid_temperature(temperature) and is_valid_humidity(humidity):
            if ts in timestamps:
                duplicate_records.append(i)
                continue
            timestamps.add(ts)
            kept_records.append(i)
        else:
            rejected_records.append(i)

    kept_records.sort(
        key=lambda record: datetime.strptime(
            record["timestamp"], "%Y-%m-%dT%H:%M"
        )
    )

    return kept_records, rejected_records, duplicate_records

def create_record_csv(file_name, header, data):
    with open(f"{file_name}.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

def main():
    try:
        response = requests.get(URL, timeout=(5, 15))
        response.raise_for_status()

        data = response.json()

        with open("raw_weather.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        records = convert_to_records(data)
        print(f"Number of records: {len(records)}")
        print(records[:2])
        print(records[-1])

        print(f"\n {"-" * 10} \n")

        kept, rejected, duplicates = clean_records(records)
        print(f"Number of kept records: {len(kept)}")
        print(f"Number of rejected records: {len(rejected)}")
        print(f"Number of duplicate records: {len(duplicates)}")

        headers = ["timestamp", "temperature_c", "humidity_pct"]
        create_record_csv("clean_weather", headers, kept)

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


if __name__ == "__main__":
    main()



