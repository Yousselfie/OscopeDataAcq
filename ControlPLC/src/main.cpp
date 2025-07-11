#include <Arduino.h>
#include <mainReader.h>


// CURRENTLY SET UP FOR TESTING ANALOG READING THE ANALOG OUTPUT OF THE PLC
// To use normally:
// Remove all the code in setup and loop
// In setup: call "setupReader()"
// In loop: call "loopReader()"

// Then, after uploading the code to the MCU, run one of the python_controllers from the folder with the same name

void setup(){
    Serial.begin(9600);
    Serial.println("Starting...");
    
    // Define mode of analog pin
    pinMode(A0, INPUT);

    // Define mode of digital pina
    for (int i=2; i<10; i++){
        pinMode(i, OUTPUT);
    }
}

void loop(){
    //Set on and print voltage
    for (int i = 2; i<10; i++){
        digitalWrite(i, LOW);    
    }
    
    //Wait 4 seconds until logic change, then print voltage again
    delay(5000);
    printVoltage();

    //Wait 8 seconds until logic change, then print voltage again
    delay(5000);
    printVoltage();

    delay(3000);

    //Set off
    for (int i = 2; i<10; i++){
        digitalWrite(i, HIGH);
    }
    printVoltage();

    //Wait 10 seconds 
    delay(5000);
    
}

