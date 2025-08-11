#pragma once // prevents "double inclusion" errors
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <Arduino.h>
#include <stdbool.h>


void setupTraffic();
void loopTraffic();
bool isOn(uint8_t pin);