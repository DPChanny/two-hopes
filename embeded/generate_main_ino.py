import requests
import json

CROP_ID = 1

API_URL = f"http://3.26.202.82:8000/api/crop/{CROP_ID}"
PIN_MAP_PATH = "pin_map.json"
ARDUINO_FILE_PATH = "main.ino"


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
        merged.append(
            {
                "sensor_id": sid,
                "sensor_type": id_to_type[sid],
                "pin": item["pin"],
            }
        )
    return merged


def write_arduino_file(sensors):
    use_dht = any(
        s["sensor_type"] in ["temperature", "humidity"] for s in sensors
    )

    lines = []
    if use_dht:
        lines.append("#include <DHT.h>")
        lines.append("#define DHTPIN 8")
        lines.append("#define DHTTYPE DHT22")
        lines.append("DHT dht(DHTPIN, DHTTYPE);")
        lines.append("")

    lines.append("struct Sensor {")
    lines.append("  int sensor_id;")
    lines.append("  String sensor_type;")
    lines.append("  int pin;")
    lines.append("};")
    lines.append("")
    lines.append(f"Sensor sensors[{len(sensors)}];")
    lines.append("")
    lines.append("void setup() {")
    lines.append("  Serial.begin(9600);")
    if use_dht:
        lines.append("  dht.begin();")
    for i, s in enumerate(sensors):
        lines.append(
            f'  sensors[{i}] = {{ {s["sensor_id"]}, "{s["sensor_type"]}", {s["pin"]} }};'
        )
    lines.append("}")
    lines.append("")
    lines.append("float readSensor(String type, int pin) {")
    lines.append('  if (type == "temperature") return dht.readTemperature();')
    lines.append('  if (type == "humidity") return dht.readHumidity();')
    lines.append('  if (type == "light") {')
    lines.append("    int analogValue = analogRead(pin);")
    lines.append("    float voltage = analogValue * (5.0 / 1023.0);")
    lines.append("    return (voltage > 0) ? 500.0 / voltage : 0;")
    lines.append("  }")
    lines.append('  if (type == "soil_moisture") {')
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


if __name__ == "__main__":
    sensors = fetch_sensors()
    pin_map = load_pin_map()
    merged = merge_sensor_data(sensors, pin_map)
    write_arduino_file(merged)
