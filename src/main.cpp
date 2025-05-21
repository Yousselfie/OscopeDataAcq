#include <Arduino.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>



void setup() {
  
  //PLC Inputs 0-7 --- digital pins 2-9
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);

  //PLC Outputs 0-7
  pinMode(22, INPUT);
  pinMode(24, INPUT);
  pinMode(26, INPUT);
  pinMode(28, INPUT);
  pinMode(30, INPUT);
  pinMode(32, INPUT);
  pinMode(34, INPUT);
  pinMode(36, INPUT);

  Serial.begin(9600);
  Serial.println("Starting...");
}

void loop() {
  if (Serial.available() > 0){
    String path_num = Serial.readStringUntil('\n');
    String header = Serial.readStringUntil('\n');
    String inputs = Serial.readStringUntil('\n');
    String outputs = Serial.readStringUntil('\n');
    String timers = Serial.readStringUntil('\n');
    
    Serial.print("Path ");
    Serial.println(path_num);
    Serial.println(header);
    Serial.println(inputs);
    Serial.println(outputs);
    Serial.println(timers);

    //------------------Extracting input values------------------//
    
    
    //Removing curly braces from input string
    int startIdx = inputs.indexOf('{');
    int endIdx = inputs.indexOf('}');
    String input_content = inputs.substring(startIdx+1, endIdx);


    //Looping to get keys and value pairs (ex: IN0 : True)
    int pos = 0;
    int current_input_pin = 2;
    while (true) {
      int commaIdx = input_content.indexOf(',', pos);
      String pair;
      if (commaIdx == -1) {
        pair = input_content.substring(pos); // last pair
      } else {
        pair = input_content.substring(pos, commaIdx);
        pos = commaIdx + 1;
      }

      // Trim spaces
      pair.trim();

      //Extracting key and value
      int quoteStart = pair.indexOf('\'') + 1;
      int quoteEnd = pair.indexOf('\'', quoteStart);
      String key = pair.substring(quoteStart, quoteEnd);

      int colonIdx = pair.indexOf(':', quoteEnd);
      String value = pair.substring(colonIdx + 1);
      value.trim();
      
      //Work with the current value
      //Set the input to the PLC ON if value is True
      if (value == "True"){
        //digitalWrite(current_input_pin, HIGH);
        Serial.print("PLC input turned ON: ");
        Serial.print(current_input_pin);
        Serial.print(" (");
        Serial.print(key);
        Serial.println(")");
      }
      //Set the input to the PLC OFF if value is False
      else{
        //digitalWrite(current_input_pin, LOW);
        Serial.print("PLC input turned OFF: ");
        Serial.print(current_input_pin);
        Serial.print(" (");
        Serial.print(key);
        Serial.println(")");
      }

      //Move to next pin
      current_input_pin = current_input_pin + 1;

      
      if (commaIdx == -1) break;
    }

    //Print a new line
    Serial.println();

  }
}