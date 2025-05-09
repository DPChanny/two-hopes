# 3. serial_update_from_config.py – config.json 기반으로 시리얼 수신 → 서버 업데이트

import argparse
import json
import serial
import requests


def load_config(path):
    with open(path, "r") as f:
        config = json.load(f)
    required = ["crop_id", "com", "pins"]
    for key in required:
        if key not in config:
            raise ValueError(f"Missing config key: '{key}'")
    return config


def parse_line(line: str):
    try:
        sensor_id, value = line.strip().split(":")
        return int(sensor_id), float(value)
    except ValueError:
        print(f"[Parse Failed] Raw: '{line.strip()}'")
        return None, None


def send_to_server(api_base_url: str, sensor_id: int, value: float):
    url = f"{api_base_url.rstrip('/')}/sensor/{sensor_id}"
    payload = {"value": str(value)}
    try:
        res = requests.patch(url, json=payload, timeout=2)
        if res.status_code == 200:
            print(f"[OK] sensor_id={sensor_id}, value={value}")
        else:
            print(f"[Failed] sensor_id={sensor_id}, status={res.status_code}")
    except requests.RequestException as e:
        print(f"[Error] sensor_id={sensor_id}, exception={e}")


def listen_serial(com: str, api_base_url: str, baud: int = 9600):
    print(f"🔌 Waiting for serial on {com}...")
    try:
        with serial.Serial(com, baud, timeout=2) as ser:
            print(f"✅ Connected to {com} ({baud} baud)")
            while True:
                try:
                    line = ser.readline().decode("utf-8").strip()
                    if not line:
                        continue
                    sensor_id, value = parse_line(line)
                    if sensor_id is not None:
                        send_to_server(api_base_url, sensor_id, value)
                except UnicodeDecodeError:
                    print("[Decode Error] Invalid serial data")
    except serial.SerialException as e:
        print(f"[Serial Error] {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Listen to serial and update server based on config.json"
    )
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument(
        "--api-base-url",
        default="http://3.26.202.82:8000/api/",
        help="Sensor update API endpoint",
    )

    args = parser.parse_args()
    config = load_config(args.config)
    listen_serial(config["com"], args.api_base_url)


if __name__ == "__main__":
    main()
