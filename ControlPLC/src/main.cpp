#include <Arduino.h>
#include <main.h>

struct KeyValuePair{
    int pos; // Since the position needs to be updated between iterations of the key-value pair extraction loop
    String key;
    String value;
};


void setup() { 
  Serial.begin(9600);
  Serial.println("Starting...");

  // Set pin mode of arduino's analog input pins
  for (int i=0; i<num_outputs; i++){
    pinMode(outputs[i], INPUT);
  }
}

void loop(){

    // Get the ordered lines of data from python
    if (Serial.available() > 0){
        String path_num = Serial.readStringUntil('\n');
        String header = Serial.readStringUntil('\n');
        String inputs_str = Serial.readStringUntil('\n');
        String outputs_str = Serial.readStringUntil('\n');
        String timers = Serial.readStringUntil('\n');
        
        Serial.print("Path ");
        Serial.println(path_num);
        Serial.println(header);
        Serial.println(inputs_str);
        Serial.println(outputs_str);
        Serial.println(timers);


        //------------------Extracting input values------------------//
        
        
        //Removing curly braces from input string
        int startIdx = inputs_str.indexOf('{');
        int endIdx = inputs_str.indexOf('}');
        String input_content = inputs_str.substring(startIdx+1, endIdx);

        //Removing curly braces from output string
        startIdx = outputs_str.indexOf('{');
        endIdx = outputs_str.indexOf('}');
        String output_content = outputs_str.substring(startIdx+1, endIdx);
        

        //--------------------Setting PLC Inputs and Printing Their Values--------------------//
        Serial.println("INPUTS:");
        int pos = 0;
        for(int current_input_pin = 2; current_input_pin<MAX_INPUT_PIN; current_input_pin++){ // 9 inputs on TM221 without added modules
            // Set Arduino pin to be an output that the PLC will input
            pinMode(current_input_pin, OUTPUT);

            // Returns a struct containing the key and value extracted from the input string
            KeyValuePair input_key_value_pair  = getKeyValuePair(input_content, pos);

            // Update the key and value with the ones returned in the struct.
            String key = input_key_value_pair.key;
            String value = input_key_value_pair.value;
            // Update the position with the one returned in the struct. This will be used in the next loop iteration if there is more to extract.
            pos = input_key_value_pair.pos;

            // Using the key and value extract from the input string and stored in key_value_pair:
            // set the PLC input (Arduino output)
            // The below function will also print the updates to the inputs in the serial monitor as they are made. 
            setPLCInput(current_input_pin, key, value);

        }

        Serial.println(); // New line


        pos = 0;
        Serial.println("OUTPUTS:");
        for (int i=0; i<num_outputs; i++){
            // Get the key-value pairs for the output string as we did for the input string in the for loop above
            
            // Returns a struct containing the key and value extracted from the input string
            KeyValuePair output_key_value_pair  = getKeyValuePair(output_content, pos);

            // Update the key and value with the ones returned in the struct.
            String key = output_key_value_pair.key;
            String value = output_key_value_pair.value;
            // Update the position with the one returned in the struct. This will be used in the next loop iteration if there is more to extract.
            pos = output_key_value_pair.pos;

            bool expectedOutput = output_key_value_pair.value == "True"; // Converting the string value to a boolean
            bool actualOutput = getPLCOutput(outputs[i]); // True or False for ON/OFF of output

            //--------------------Reading PLC Outputs and Printing Their Values--------------------//
            if (actualOutput){
                Serial.print(outputs[i]);
                Serial.print(" (");
                Serial.print("Q");
                Serial.print(i);
                Serial.print(")");
                Serial.print(" ON");
            }
            else{
                Serial.print(outputs[i]);
                Serial.print(" (");
                Serial.print("Q");
                Serial.print(i);
                Serial.print(")");
                Serial.print(" OFF");
            }
            //--------------------Printing If They Are as Expected--------------------//
            if (checkPLCOutput(actualOutput, expectedOutput)){
                Serial.println(" -> ✓");
            }
            else{
                Serial.println(" -> ✕");
            }
        }

        Serial.println(); // New line

    }

}

bool checkPLCOutput(bool actual, bool expected){
    return actual == expected;
}

// Returns true for ON and false for OFF
bool getPLCOutput(uint8_t output){
    int sensorValue = analogRead(output); // Read arduino analog input (will be between 0-1023)
    float voltage = sensorValue * (4.665 / 1023.0); // Convert raw sensor value to voltage
    // (~4.6 is the maximum voltage allowed by the circuit that the PLC output voltage travels through)
    // ...thus, if the voltage is at this level, the output is considered on
    return voltage >= 4.6;    
}

void setPLCInput(int current_input_pin, String key, String value){
    //Set the input to the PLC ON if value is True
    if (value == "True"){
        digitalWrite(current_input_pin, LOW);

        Serial.print(current_input_pin);
        Serial.print(" (");
        Serial.print(key);
        Serial.print("):");
        Serial.println(" ON");
    }
    //Set the input to the PLC OFF if value is False
    else{
        digitalWrite(current_input_pin, HIGH);
        
        Serial.print(current_input_pin);
        Serial.print(" (");
        Serial.print(key);
        Serial.print("):");
        Serial.println(" OFF");
    }
}

KeyValuePair getKeyValuePair(String content, int pos){

    // Instantiating the struct to be returned containing the extracted key and value
    KeyValuePair pair;

    //Getting the key, value pair
    int commaIdx = content.indexOf(',', pos);
    String pair_str;
    if (commaIdx == -1) {
        pair_str = content.substring(pos); // last pair_str
    } else {
        pair_str = content.substring(pos, commaIdx);
        pos = commaIdx + 1;
    }

    // Trim spaces
    pair_str.trim();

    //Extracting key and value
    int quoteStart = pair_str.indexOf('\'') + 1;
    int quoteEnd = pair_str.indexOf('\'', quoteStart);
    String key = pair_str.substring(quoteStart, quoteEnd);

    int colonIdx = pair_str.indexOf(':', quoteEnd);
    String value = pair_str.substring(colonIdx + 1);
    value.trim();

    // Initializing and returning the key-value pair
    pair.key = key;
    pair.value = value;

    // Update the position to start from in the next iteration
    pair.pos = pos;

    return pair;
}


