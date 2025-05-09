import subprocess
import requests
import json
import os
import shutil

CROP_ID = 1

API_URL = f"http://3.26.202.82:8000/api/crop/{CROP_ID}"
PIN_MAP_PATH = "pin_map.json"
SKETCH_DIR = "main"
ARDUINO_FILE_PATH = os.path.join(SKETCH_DIR, "main.ino")

BOARD = "arduino:avr:uno"
PORT = "COM5"
LIBRARIES = ["DHT sensor library", "Adafruit Unified Sensor"]


def fetch_sensors():
    res = requests.get(API_URL)
    res.raise_for_status()
    return res.json()["data"]["sensors"]


def load_pin_map():
    with open(PIN_MAP_PATH, "r") as f:
        return json.load(f)


def merge_sensor_data(sensors, pin_map):
    id_to_type = {s["sensor_id"]: s["sensor_type"] for s in sensors}
    merged = []

    for item in pin_map:
        sid = item["sensor_id"]
        if sid not in id_to_type:
            raise ValueError(f"sensor_id {sid} not found in crop data")

        sensor_type = id_to_type[sid]

        if "dht_pin" in item:
            merged.append(
                {
                    "sensor_id": sid,
                    "sensor_type": sensor_type,
                    "dht_pin": item["dht_pin"],
                }
            )
        else:
            merged.append(
                {
                    "sensor_id": sid,
                    "sensor_type": sensor_type,
                    "pin": item["pin"],
                }
            )
    return merged


def write_arduino_file(sensors):
    os.makedirs(SKETCH_DIR, exist_ok=True)

    dht_sensors = [s for s in sensors if "dht_pin" in s]
    unique_dht_pins = sorted(set(s["dht_pin"] for s in dht_sensors))

    lines = []
    if unique_dht_pins:
        lines.append("#include <DHT.h>")
        for i, pin in enumerate(unique_dht_pins):
            lines.append(f"DHT dht{i}({pin}, DHT22);")
        lines.append("")

    lines.append("struct Sensor {")
    lines.append("  int sensor_id;")
    lines.append("  String sensor_type;")
    lines.append("  int pin;")
    lines.append("};")
    lines.append(f"Sensor sensors[{len(sensors)}];")
    lines.append("")
    lines.append("void setup() {")
    lines.append("  Serial.begin(9600);")
    if unique_dht_pins:
        for i in range(len(unique_dht_pins)):
            lines.append(f"  dht{i}.begin();")
    for i, s in enumerate(sensors):
        pin = s.get("dht_pin", s.get("pin"))
        lines.append(
            f'  sensors[{i}] = {{ {s["sensor_id"]}, "{s["sensor_type"]}", {pin} }};'
        )
    lines.append("}")
    lines.append("")
    lines.append("float readSensor(String type, int pin) {")

    for i, pin in enumerate(unique_dht_pins):
        lines.append(
            f'  if (pin == {pin} && type == "temperature") return dht{i}.readTemperature();'
        )
        lines.append(
            f'  if (pin == {pin} && type == "humidity") return dht{i}.readHumidity();'
        )

    lines.append('  if (type == "light") {')
    lines.append("    int analogValue = analogRead(pin);")
    lines.append(
        "    float lux = (analogValue - 400) * (600.0 / 600.0) + 100.0;"
    )
    lines.append("    return lux;")
    lines.append("  }")
    lines.append('  if (type == "water") {')
    lines.append("    int value = analogRead(pin);")
    lines.append("    int percent = map(value, 1023, 300, 0, 100);")
    lines.append("    return constrain(percent, 0, 100);")
    lines.append("  }")
    lines.append("  return 0;")
    lines.append("}")
    lines.append("")
    lines.append("void loop() {")
    lines.append(f"  for (int i = 0; i < {len(sensors)}; i++) {{")
    lines.append(
        "    float value = readSensor(sensors[i].sensor_type, sensors[i].pin);"
    )
    lines.append("    Serial.print(sensors[i].sensor_id);")
    lines.append('    Serial.print(":");')
    lines.append("    Serial.println(value);")
    lines.append("  }")
    lines.append("  delay(1000);")
    lines.append("}")

    with open(ARDUINO_FILE_PATH, "w") as f:
        f.write("\n".join(lines))
    print(f"✅ Saved {ARDUINO_FILE_PATH}")


def run_command(command: list):
    print(f"$ {' '.join(command)}")
    subprocess.run(command, check=True)


def install_libraries():
    for lib in LIBRARIES:
        run_command(["arduino-cli", "lib", "install", lib])


def compile_and_upload():
    run_command(["arduino-cli", "core", "install", "arduino:avr"])
    install_libraries()
    run_command(["arduino-cli", "compile", "--fqbn", BOARD, SKETCH_DIR])
    run_command(
        ["arduino-cli", "upload", "-p", PORT, "--fqbn", BOARD, SKETCH_DIR]
    )


if __name__ == "__main__":
    sensors = fetch_sensors()
    pin_map = load_pin_map()
    merged = merge_sensor_data(sensors, pin_map)
    write_arduino_file(merged)
    compile_and_upload()
