#pragma once // prevents "double inclusion" errors
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <Arduino.h>

//There are 54 digital pins on the **Arduino Mega**
//Each input must have an output, so there can be a maximum of 27 input and 27 output pins
//Allocate pins 0-26 for input and 27-53 for output
//*PINS THAT CAN'T BE USED: 
const int MAX_INPUT_PIN = 11;
const int MAX_OUTPUT_PIN = 53;

void setupReader();
void loopReader();