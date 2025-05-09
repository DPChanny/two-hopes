import json
import requests

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
    analog_index = 0
    dht_pin = 8

    temperature = next(
        (s for s in sensors if s["sensor_type"] == "temperature"), None
    )
    humidity = next(
        (s for s in sensors if s["sensor_type"] == "humidity"), None
    )

    if temperature and humidity:
        pin_map.append(
            {
                "sensor_id": temperature["sensor_id"],
                "sensor_type": "temperature",
                "dht_pin": dht_pin,
            }
        )
        pin_map.append(
            {
                "sensor_id": humidity["sensor_id"],
                "sensor_type": "humidity",
                "dht_pin": dht_pin,
            }
        )
    elif temperature or humidity:
        raise ValueError(
            "Both temperature and humidity must exist together for DHT"
        )

    for s in sensors:
        if s["sensor_type"] in ["temperature", "humidity"]:
            continue
        pin_map.append(
            {
                "sensor_id": s["sensor_id"],
                "sensor_type": s["sensor_type"],
                "pin": f"A{analog_index}",
            }
        )
        analog_index += 1

    return pin_map


if __name__ == "__main__":
    sensors = fetch_sensors()
    pin_map = generate_pin_map(sensors)

    with open(PIN_MAP_PATH, "w") as f:
        json.dump(pin_map, f, indent=2)
    print(f"✅ Saved {PIN_MAP_PATH}")
