// Include the Wire library for I2C
#include <Wire.h>
#include "CRC.h"
#include "Checksum.h"

String package;
String g_x;
bool gerador = false;
CRC c;
int times = 0;
String mode = "CRC";
int pack[6];
int pos = 0;
Checksum cs(4);

void setup() {
  // Join I2C bus as slave with address 8
  Wire.begin(0x8);

  // Call receiveEvent when data received
  Wire.onReceive(receiveEvent);

  Serial.begin(9600);
}

// Function that executes whenever data is received from master
void receiveEvent(int howMany)
{
  while(Wire.available()) // loop through all but the last
  {
    int c = Wire.read(); // receive byte as a character
    
    if(times == 0) // primeiro caracter é o offset, 0 pra CRC e 1 pra Checksum
    {
      times = 1;
      if(c == 0) mode = "CRC";
      else if(c == 1) mode = "CHECKSUM";
    }
    else
    {
      if(mode == "CRC")
      {
        // tem que ser nessa ordem, pq quando for 9, só descarta o valor e pega a partir do próximo
        if(gerador) g_x += String(c);
        else if(c == 9) gerador = true;
        else package += String(c);
      }
      else if(mode == "CHECKSUM")
      {
        pack[pos] = c;
        pos += 1;
      }
    }
  }
  Serial.println("-----------------MODE = " + mode + "----------------");

  if(mode == "CRC") c.decoder(package,g_x);
  else if(mode == "CHECKSUM") cs.receptor(pack);
  package = "";
  g_x = "";
  times = 0;
  pos = 0;
  gerador = false;
  c.clean();
  cs.clean();

  Serial.println("------------------------------------------------");
}

void loop() {
  delay(100);
}
