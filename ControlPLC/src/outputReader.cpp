#include <outputReader.h>

uint8_t outputs[] = {A0, A1, A2, A3};
int num_outputs = 4;

void setupOutputReader() {
  Serial.begin(9600); // Start serial communication

  // Set pin mode of arduino's analog input pins
  for (int i=0; i<num_outputs; i++){
    pinMode(outputs[i], INPUT);
  }
}

void loopOutputReader() {

  for (int i=0; i<num_outputs; i++){
    int sensorValue = analogRead(outputs[i]); // Read analog input 
    float voltage = sensorValue * (4.665 / 1023.0); // Convert to voltage

    Serial.print(outputs[i]);
    Serial.print(") ");
    Serial.print("Analog value: ");
    Serial.print(sensorValue);
    Serial.print(" => Voltage: ");
    Serial.print(voltage);
    Serial.println(" V");
  }
  
  

  delay(1000); // Wait a second
}
