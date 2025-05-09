# 1. generate_config.py – config.json 생성 스크립트

import argparse
import json
import os
import requests

DEFAULT_DHT_PIN = 8
DEFAULT_ANALOG_PREFIX = "A"


def fetch_sensors(crop_id: int, api_base_url: str):
    url = f"{api_base_url.rstrip("/")}/crop/{crop_id}"
    res = requests.get(url, timeout=5)
    res.raise_for_status()
    return res.json()["data"]["sensors"]


def generate_pin_map(sensors):
    pin_map = []
    analog_index = 0

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
                "dht_pin": DEFAULT_DHT_PIN,
            }
        )
        pin_map.append(
            {
                "sensor_id": humidity["sensor_id"],
                "sensor_type": "humidity",
                "dht_pin": DEFAULT_DHT_PIN,
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
                "pin": f"{DEFAULT_ANALOG_PREFIX}{analog_index}",
            }
        )
        analog_index += 1

    return pin_map


def main():
    parser = argparse.ArgumentParser(
        description="Generate config.json for a crop"
    )
    parser.add_argument("--crop-id", required=True, type=int)
    parser.add_argument("--com", required=True)
    parser.add_argument("--board", default="arduino:avr:uno")
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--api-base-url",
        default="http://3.26.202.82:8000/api/",
        help="Sensor update API endpoint",
    )

    args = parser.parse_args()
    os.makedirs(args.output, exist_ok=True)

    sensors = fetch_sensors(args.crop_id, args.api_base_url)
    pin_map = generate_pin_map(sensors)

    config = {
        "crop_id": args.crop_id,
        "com": args.com,
        "board": args.board,
        "pins": pin_map,
    }

    config_path = os.path.join(args.output, "config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Saved config: {config_path}")


if __name__ == "__main__":
    main()
