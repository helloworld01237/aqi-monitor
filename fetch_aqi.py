import requests
import pandas as pd
from datetime import datetime
import os
import schedule
import time

API_KEY = "450bbb14e74a86eb6e4c0e34cef3336b"

CITIES = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
    "Pilani": (28.3674, 75.6042)
}

AQI_THRESHOLD = 3

def fetch_aqi(city, lat, lon):
    try:
        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        aqi_response = requests.get(aqi_url, timeout=10).json()

        if "list" not in aqi_response:
            print(f"Unexpected response for {city}: {aqi_response}")
            return None

        aqi = aqi_response["list"][0]["main"]["aqi"]
        components = aqi_response["list"][0]["components"]
        anomaly = "Alert" if aqi >= AQI_THRESHOLD else "Normal"

        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": city,
            "aqi": aqi,
            "pm2_5": components["pm2_5"],
            "pm10": components["pm10"],
            "co": components["co"],
            "no2": components["no2"],
            "status": anomaly
        }

    except requests.exceptions.RequestException as e:
        print(f"Network error for {city}: {e}. Skipping this run.")
        return None
    except Exception as e:
        print(f"Unexpected error for {city}: {e}. Skipping this run.")
        return None

def fix_existing_csv(filename="aqi_data.csv"):
    if not os.path.exists(filename):
        return
    df = pd.read_csv(filename)
    if "status" not in df.columns:
        df["status"] = df["aqi"].apply(lambda x: "Alert" if x >= AQI_THRESHOLD else "Normal")
    else:
        df["status"] = df.apply(
            lambda row: "Alert" if row["aqi"] >= AQI_THRESHOLD else "Normal"
            if pd.isnull(row["status"]) else row["status"], axis=1
        )
    df.to_csv(filename, index=False)
    print("Fixed existing CSV status column.")

def save_to_csv(data, filename="aqi_data.csv"):
    df = pd.DataFrame([data])
    file_exists = os.path.exists(filename)
    df.to_csv(filename, mode="a", header=not file_exists, index=False)
    print(f"[{data['timestamp']}] {data['city']} — AQI: {data['aqi']} — Status: {data['status']}")

def run():
    print("Fetching AQI data...")
    for city, (lat, lon) in CITIES.items():
        data = fetch_aqi(city, lat, lon)
        if data:
            save_to_csv(data)
    print("Done. Next run in 1 hour.\n")

# Fix nulls in existing CSV first
fix_existing_csv()

# Run immediately once, then every hour
run()
schedule.every(1).hours.do(run)

print("Scheduler running. Keep this window open. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)