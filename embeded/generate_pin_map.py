import requests
import json

CROP_ID = 1
API_URL = f"http://3.26.202.82:8000/api/crop/{CROP_ID}"
PIN_MAP_PATH = "pin_map.json"
DEFAULT_PIN_PREFIX = "A"


def fetch_sensors():
    res = requests.get(API_URL)
    res.raise_for_status()
    return res.json()["data"]["sensors"]


def generate_pin_map(sensors):
    pin_map = []
    for i, sensor in enumerate(sensors):
        pin_map.append(
            {
                "pin": f"{DEFAULT_PIN_PREFIX}{i}",
                "sensor_id": sensor["sensor_id"],
            }
        )
    with open(PIN_MAP_PATH, "w") as f:
        json.dump(pin_map, f, indent=2)
    print(f"✅ Generated {PIN_MAP_PATH}")


if __name__ == "__main__":
    sensors = fetch_sensors()
    generate_pin_map(sensors)
