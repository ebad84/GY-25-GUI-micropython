
//float Roll,Pitch,Yaw;
byte databyte;
//byte RFin_bytes[68];

void setup() 
{
  Serial.begin(9600);             // Serial port to computer
  Serial1.begin(9600);               // Serial port to HC12
}

void loop()
{
  if(Serial1.available())
  {
    byte a = Serial1.read();
    Serial.write(a);
//    databyte = Serial1.read();
//    Serial.write(databyte);
    //delay (1000);
  }
}

//void loop() 
//{
// int availableBytes = Serial1.available();
// Serial.println(availableBytes);
//}

//void loop() 
//{ 
//  int availableBytes =  Serial1.available();
//  while (availableBytes < 69) {} // Wait 'till1 there are 9 Bytes waiting
//  for(int n=0; n<68; n++)
//  {
//    RFin_bytes[n] = Serial1.read(); // Then: Get them.
//    Serial.print(RFin_bytes[n]);  
//  }
//}
