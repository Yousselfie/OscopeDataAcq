#include <Arduino.h>
#include <new_main.h>

struct inputKeyValuePair{
    int pos; // Since the position needs to be updated between iterations of the key-value pair extraction loop
    String key;
    String value;
};


void setup() { 
  Serial.begin(9600);
  Serial.println("Starting...");
}

void loop(){

    // Get the ordered lines of data from python
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

        int pos = 0;
        for(int current_input_pin = 2; current_input_pin++; current_input_pin<MAX_INPUT_PIN){ // 9 inputs on TM221 without added modules
            // Set Arduino pin to be an output that the PLC will input
            pinMode(current_input_pin, OUTPUT);

            // Returns a struct containing the key and value extracted from the input string
            inputKeyValuePair key_value_pair  = getInputKeyValuePair(input_content, pos);

            // Update the key and value with the ones returned in the struct.
            String key = key_value_pair.key;
            String value = key_value_pair.value;
            // Update the position with the one returned in the struct. This will be used in the next loop iteration if there is more to extract.
            pos = key_value_pair.pos;

            // Using the key and value extract from the input string and stored in key_value_pair:
            // set the PLC input (Arduino output)
            // The below function will also print the updates to the inputs in the serial monitor as they are made. 
            setPLCInput(current_input_pin, key, value);

        }

    }

}

void setPLCInput(int current_input_pin, String key, String value){
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
}

inputKeyValuePair getInputKeyValuePair(String input_content, int pos){

    // Instantiating the struct to be returned containing the extracted key and value
    inputKeyValuePair pair;

    //Getting the key, value pair
    int commaIdx = input_content.indexOf(',', pos);
    String pair_str;
    if (commaIdx == -1) {
        pair_str = input_content.substring(pos); // last pair_str
    } else {
        pair_str = input_content.substring(pos, commaIdx);
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

