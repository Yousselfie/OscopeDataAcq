#pragma once // prevents "double inclusion" errors
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <Arduino.h>
#include <stdbool.h>

struct KeyValuePair;

const int MAX_INPUT_PIN = 10; //starting at pin 2, this makes 9 input pins

const uint8_t outputs[] = {A0, A1, A2, A3};
const int num_outputs = 4;

void setupReader();
void loopReader();
KeyValuePair getKeyValuePair(String input_content, int pos);
void setPLCInput(int current_input_pin, String key, String value);
bool getPLCOutput(uint8_t output);
bool checkPLCOutput(bool actual, bool expected); // Check actual output value vs expected, return true if they match
void printVoltage();