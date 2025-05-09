import argparse
import json
import serial
import requests
import time


def load_config(config_path):
    with open(config_path, "r") as f:
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


def listen_serial(
    com: str, api_base_url: str, baud: int = 9600, interval_sec: float = 2.5
):
    print(f"🔌 Waiting for serial on {com}...")
    try:
        with serial.Serial(com, baud, timeout=1) as ser:
            print(f"Connected to {com} ({baud} baud)")

            latest_values = {}  # sensor_id: value
            last_sent = time.time()

            while True:
                now = time.time()

                # 시리얼 데이터 수신
                if ser.in_waiting:
                    try:
                        line = ser.readline().decode("utf-8").strip()
                        if line:
                            sensor_id, value = parse_line(line)
                            if sensor_id is not None:
                                latest_values[sensor_id] = value
                    except UnicodeDecodeError:
                        print("[Decode Error] Invalid serial data")

                # 전송 타이밍 도달
                if now - last_sent >= interval_sec:
                    if latest_values:
                        print(
                            f"\n⏱ Sending {len(latest_values)} sensor(s) to server..."
                        )
                        for sid, val in latest_values.items():
                            send_to_server(api_base_url, sid, val)
                        latest_values.clear()
                    last_sent = now

    except serial.SerialException as e:
        print(f"[Serial Error] {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Listen to serial and update server every N seconds based on config.json"
    )
    parser.add_argument(
        "--config-path", required=True, help="Path to config.json"
    )
    parser.add_argument(
        "--api-base-url",
        default="http://3.26.202.82:8000/api/",
        help="Sensor update API endpoint",
    )
    parser.add_argument(
        "--interval", type=int, default=5, help="Send interval in seconds"
    )

    args = parser.parse_args()
    config = load_config(args.config_path)
    listen_serial(config["com"], args.api_base_url, interval_sec=args.interval)


if __name__ == "__main__":
    main()
