#include <Arduino.h>

void setup() {
  Serial.begin(115200); // open serial connection to USB Serial port (connected to your computer)
  Serial1.begin(57600); // open internal serial connection to MT7688AN
  // in MT7688AN, this maps to device
  pinMode(4, OUTPUT);
}
void loop() {
  int c = Serial.read(); // read from MT7688AN
  if (c != -1) {
    switch(c) {
      case '0': // turn off D13 when receiving "0"
        digitalWrite(4, 0);
        break;
      case '1': // turn off D13 when receiving "1"
        digitalWrite(4, 1);
      break;
    }
  }
}
