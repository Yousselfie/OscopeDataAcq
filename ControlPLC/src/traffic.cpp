#include <traffic.h>
#include <mainReader.h>

unsigned long start;

// Keeps checking for output changes and logs them

void setupTraffic(){
    Serial.begin(9600);
    Serial.println("Starting...");
    start = millis();

    // Define mode of output pins
    pinMode(A4, INPUT);
    pinMode(A1, INPUT);
    pinMode(A2, INPUT);
    pinMode(A3, INPUT);

    // Define mode of input pin
    pinMode(2, OUTPUT);
}

void loopTraffic(){
    
    //Turn on
    digitalWrite(2, LOW);

    delay(0.5);

    //Run for 10 seconds
    while ((millis() - start) < 10000){
        //Loop through all outputs and check if an output is on
        for (int i = 0; i<num_outputs; i++){
            if(isOn(outputs[i])){
                Serial.print("Q");
                Serial.print(i);
                Serial.print(": is ON at ");
                Serial.print(millis() - start);
                Serial.println("ms");
            }
        }
    }

    // Turn off for 8 seconds
    digitalWrite(2, HIGH);
    delay(0.5);
    if(isOn(outputs[0])){
        Serial.print("Q");
        Serial.print(0);
        Serial.print(": is ON at ");
        Serial.print(millis() - start);
        Serial.println("ms");
    }
    delay(8000);
}



bool isOn(uint8_t pin){
    return analogRead(pin) >= 900;
}

