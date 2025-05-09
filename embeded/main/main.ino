#include <DHT.h>
DHT dht0(8, DHT22);

struct Sensor {
  int sensor_id;
  String sensor_type;
  int pin;
};
Sensor sensors[3];

void setup() {
  Serial.begin(9600);
  dht0.begin();
  sensors[0] = { 1, "temperature", 8 };
  sensors[1] = { 2, "humidity", 8 };
  sensors[2] = { 3, "light", A0 };
}

float readSensor(String type, int pin) {
  if (pin == 8 && type == "temperature") return dht0.readTemperature();
  if (pin == 8 && type == "humidity") return dht0.readHumidity();
  if (type == "light") {
    int analogValue = analogRead(pin);
    float lux = (analogValue - 400) * (600.0 / 600.0) + 100.0;
    return lux;
  }
  if (type == "water") {
    int value = analogRead(pin);
    int percent = map(value, 1023, 300, 0, 100);
    return constrain(percent, 0, 100);
  }
  return 0;
}

void loop() {
  for (int i = 0; i < 3; i++) {
    float value = readSensor(sensors[i].sensor_type, sensors[i].pin);
    Serial.print(sensors[i].sensor_id);
    Serial.print(":");
    Serial.println(value);
  }
  delay(1000);
}