# 2. generate_main_from_config.py – config.json 기반으로 main.ino 생성만

import argparse
import json
import os


def load_config(path):
    with open(path, "r") as f:
        config = json.load(f)
    required = ["crop_id", "com", "board", "pins"]
    for key in required:
        if key not in config:
            raise ValueError(f"Missing config key: '{key}'")
    return config


def write_arduino_file(sensors, sketch_dir):
    os.makedirs(sketch_dir, exist_ok=True)
    ino_path = os.path.join(sketch_dir, "main.ino")

    dht_pins = sorted({s["dht_pin"] for s in sensors if "dht_pin" in s})
    lines = []

    if dht_pins:
        lines.append("#include <DHT.h>")
        for i, pin in enumerate(dht_pins):
            lines.append(f"DHT dht{i}({pin}, DHT22);")
        lines.append("")

    lines.append(
        "struct Sensor { int sensor_id; String sensor_type; int pin; };"
    )
    lines.append(f"Sensor sensors[{len(sensors)}];")
    lines.append("")
    lines.append("void setup() {")
    lines.append("  Serial.begin(9600);")
    for i, pin in enumerate(dht_pins):
        lines.append(f"  dht{i}.begin();")
    for i, s in enumerate(sensors):
        pin = s.get("dht_pin", s.get("pin"))
        lines.append(
            f'  sensors[{i}] = {{ {s["sensor_id"]}, "{s["sensor_type"]}", {pin} }};'
        )
    lines.append("}")
    lines.append("")
    lines.append("float readSensor(String type, int pin) {")
    for i, pin in enumerate(dht_pins):
        lines.append(
            f'  if (pin == {pin} && type == "temperature") return dht{i}.readTemperature();'
        )
        lines.append(
            f'  if (pin == {pin} && type == "humidity") return dht{i}.readHumidity();'
        )
    lines.append(
        '  if (type == "light") { int a = analogRead(pin); return (a - 400) * (600.0 / 600.0) + 100; }'
    )
    lines.append(
        '  if (type == "water") { int v = analogRead(pin); return constrain(map(v, 1023, 300, 0, 100), 0, 100); }'
    )
    lines.append("  return 0;")
    lines.append("}")
    lines.append("")
    lines.append("void loop() {")
    lines.append(f"  for (int i = 0; i < {len(sensors)}; i++) {{")
    lines.append(
        "    float v = readSensor(sensors[i].sensor_type, sensors[i].pin);"
    )
    lines.append(
        '    Serial.print(sensors[i].sensor_id); Serial.print(":"); Serial.println(v);'
    )
    lines.append("  }")
    lines.append("  delay(1000);")
    lines.append("}")

    with open(ino_path, "w") as f:
        f.write("\n".join(lines))
    print(f"Saved: {ino_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate main.ino from config.json"
    )
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument(
        "--output", required=True, help="Directory to write sketch"
    )
    args = parser.parse_args()

    config = load_config(args.config)
    sensors = config["pins"]
    sketch_dir = os.path.join(args.output, "main")
    write_arduino_file(sensors, sketch_dir)


if __name__ == "__main__":
    main()
