#include <DHT.h>
#define DHTPIN 8
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

struct Sensor {
  int sensor_id;
  String sensor_type;
  int pin;
};

Sensor sensors[2];

void setup() {
  Serial.begin(9600);
  dht.begin();
  sensors[0] = {1, "temperature", A0};
  sensors[1] = {2, "humidity", A1};
}

float readSensor(String type, int pin) {
  if (type == "temperature")
    return dht.readTemperature();
  if (type == "humidity")
    return dht.readHumidity();
  if (type == "light") {
    int analogValue = analogRead(pin);
    float voltage = analogValue * (5.0 / 1023.0);
    return (voltage > 0) ? 500.0 / voltage : 0;
  }
  if (type == "soil_moisture") {
    int value = analogRead(pin);
    int percent = map(value, 1023, 300, 0, 100);
    return constrain(percent, 0, 100);
  }
  return 0;
}

void loop() {
  for (int i = 0; i < 2; i++) {
    float value = readSensor(sensors[i].sensor_type, sensors[i].pin);
    Serial.print(sensors[i].sensor_id);
    Serial.print(":");
    Serial.println(value);
  }
  delay(1000);
}