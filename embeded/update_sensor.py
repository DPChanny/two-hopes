import serial
import requests

SERIAL_PORT = "COM5"
BAUD_RATE = 9600
API_BASE_URL = "http://3.26.202.82:8000/api/sensor/"


def parse_line(line: str):
    try:
        sensor_id, value = line.strip().split(":")
        return int(sensor_id), float(value)
    except ValueError:
        print(f"Parse failed: '{line.strip()}'")
        return None, None


def send_to_server(sensor_id: int, value: float):
    url = f"{API_BASE_URL}{sensor_id}"
    payload = {"value": str(value)}
    try:
        response = requests.patch(url, json=payload, timeout=2)
        if response.status_code == 200:
            print(f"Updated: sensor_id={sensor_id}, value={value}")
        else:
            print(
                f"Update failed: sensor_id={sensor_id}, status={response.status_code}"
            )
    except requests.RequestException as e:
        print(f"Request error: sensor_id={sensor_id}, error={e}")


def main():
    print("Waiting for serial connection...")
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
            print(f"Connected: {SERIAL_PORT}, {BAUD_RATE}bps")
            while True:
                try:
                    line = ser.readline().decode("utf-8").strip()
                    if not line:
                        continue
                    sensor_id, value = parse_line(line)
                    if sensor_id is not None:
                        send_to_server(sensor_id, value)
                except UnicodeDecodeError:
                    print("Decode error: invalid serial data")
    except serial.SerialException as e:
        print(f"Serial open failed: {e}")


if __name__ == "__main__":
    main()
