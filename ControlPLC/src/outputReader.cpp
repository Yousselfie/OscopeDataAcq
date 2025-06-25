#include <outputReader.h>

void setupOutputReader() {
  Serial.begin(9600); // Start serial communication
  pinMode(A5, INPUT);
}

void loopOutputReader() {
  int sensorValue = analogRead(A5); // Read analog input on pin A0
  float voltage = sensorValue * (4.61 / 1023.0); // Convert to voltage

  Serial.print("Analog value: ");
  Serial.print(sensorValue);
  Serial.print(" => Voltage: ");
  Serial.print(voltage);
  Serial.println(" V");

  delay(500); // Wait half a second
}
