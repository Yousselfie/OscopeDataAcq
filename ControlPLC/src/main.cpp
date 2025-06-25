#include <mainReader.h>
#include <outputReader.h>
#include <Arduino.h>

void setup() {
  // Set all PLC inputs on for testing 
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);

  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  digitalWrite(6, LOW);

  
  setupOutputReader();
}

void loop() {
  loopOutputReader();
}