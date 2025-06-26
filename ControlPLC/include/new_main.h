#pragma once // prevents "double inclusion" errors
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <Arduino.h>

struct inputKeyValuePair;

inputKeyValuePair getInputKeyValuePair(String input_content, int pos);
void setPLCInput(int current_input_pin, String key, String value);