#include <EEPROM.h>

// start reading from the first byte (address 0) of the EEPROM
const int dataSize = 190;
byte value;
byte eeprom_data[dataSize] = {
  205, 204, 204, 61, 23, 183, 209, 56, 23, 183, 209, 56, 0, 0, 250, 68, 39, 155, 32, 68, 86, 193, 2, 0, 0, 0, 192, 64, 1, 188, 116, 147, 60, 10, 215, 35, 61, 0,
  205, 204, 204, 61, 23, 183, 209, 56, 23, 183, 209, 56, 0, 0, 250, 68, 39, 155, 32, 68, 86, 193, 2, 0, 0, 0, 192, 64, 1, 188, 116, 147, 60, 10, 215, 35, 61, 0,
  205, 204, 204, 61, 23, 183, 209, 56, 23, 183, 209, 56, 0, 0, 250, 68, 39, 155, 32, 68, 86, 193, 2, 0, 0, 0, 192, 64, 1, 188, 116, 147, 60, 10, 215, 35, 61, 0,
  205, 204, 204, 61, 23, 183, 209, 56, 23, 183, 209, 56, 0, 0, 250, 68, 39, 155, 32, 68, 86, 193, 2, 0, 0, 0, 192, 64, 1, 188, 116, 147, 60, 10, 215, 35, 61, 0,
  205, 204, 204, 61, 23, 183, 209, 56, 23, 183, 209, 56, 0, 0, 250, 68, 39, 155, 32, 68, 86, 193, 2, 0, 0, 0, 192, 64, 1, 188, 116, 147, 60, 10, 215, 35, 61, 0
};

void setup()
{
  Serial.begin(250000);
  for (int address=0; address<dataSize;address++ ){
    // read a byte from the current address of the EEPROM
    value = eeprom_data[address];
    EEPROM.write(address, value);

    Serial.print(address);
    Serial.print("\t");
    Serial.print(value, DEC);
    Serial.println();


  // there are only 512 bytes of EEPROM, from 0 to 511, so if we're
  // on address 512, wrap around to address 0
  }
}

void loop(){
}





