#include <Arduino.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

//There are 54 digital pins on the **Arduino Mega**
//Each input must have an output, so there can be a maximum of 27 input and 27 output pins
//Allocate pins 0-26 for input and 27-53 for output
//*PINS THAT CAN'T BE USED: 
const int MAX_INPUT_PIN = 26;
const int MAX_OUTPUT_PIN = 53;

void setup() { 
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

    //------------------------------------Setting/Reading PLC Input------------------------------------//

    //------------------Extracting input values------------------//
    
    
    //Removing curly braces from input string
    int startIdx = inputs.indexOf('{');
    int endIdx = inputs.indexOf('}');
    String input_content = inputs.substring(startIdx+1, endIdx);


    //Looping to get keys and value pairs (ex: IN0 : True)
    int pos = 0;
    int current_input_pin = 2;
    while (current_input_pin <= MAX_INPUT_PIN) {

      //Set pin to output signal from Arduino to PLC
      pinMode(current_input_pin, OUTPUT);
      
      //Getting the key, value pair
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
        digitalWrite(current_input_pin, LOW);
        Serial.print("PLC input turned ON: ");
        Serial.print(current_input_pin);
        Serial.print(" (");
        Serial.print(key);
        Serial.println(")");
      }
      //Set the input to the PLC OFF if value is False
      else{
        digitalWrite(current_input_pin, HIGH);
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

    //------------------------------------Reading/Checking PLC Output------------------------------------//

    //------------------Extracting output values------------------//


    //Removing curly braces from input string
    startIdx = outputs.indexOf('{');
    endIdx = outputs.indexOf('}');
    String output_content = outputs.substring(startIdx+1, endIdx);


    //Looping to get keys and value pairs (ex: IN0 : True)
    pos = 0;
    int current_output_pin = 22;
    while (current_output_pin <= MAX_OUTPUT_PIN) {

      //Set pin to input signal from PLC to Arduino
      pinMode(current_output_pin, INPUT);

      //Getting the key, value pair
      int commaIdx = output_content.indexOf(',', pos);
      String pair;
      if (commaIdx == -1) {
        pair = output_content.substring(pos); // last pair
      } else {
        pair = output_content.substring(pos, commaIdx);
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
      //Check that the PLC output is consistent with the expected output (value)
      //HIGH(1) == True, LOW(0) == False
      String actual_output = (digitalRead(current_output_pin) == 1) ? "ON" : "OFF";
      String expected_output = "True" ? "ON" : "OFF"; 
      if (actual_output == expected_output){
        Serial.print("CORRECT OUTPUT: ");
        Serial.print(current_output_pin);
        Serial.print(" (");
        Serial.print(key);
        Serial.println(")");
      }
      else{
          
        Serial.print("WRONG OUTPUT: Pin ");
        Serial.print(current_output_pin);
        Serial.print(" (");
        Serial.print(key);
        Serial.print(") should be ");
        Serial.println(expected_output);
      }

      //Move to next pin
      current_output_pin = current_output_pin + 1;

      
      if (commaIdx == -1) break;
    }


    //Print a new line
    Serial.println();

  }
}