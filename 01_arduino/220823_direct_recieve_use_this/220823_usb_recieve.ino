
// Connect RX of GY 25 to TX3 Arduino Mega and TX of GY 25 to RX3 Arduino Mega

#include <SoftwareSerial.h>
float Roll,Pitch,Yaw;
unsigned char Re_buf[8],counter=0;

void setup()
{
Serial.begin(9600);
Serial3.begin(9600);

  // set GY
  delay(4000);
  Serial3.write(0XA5);
  Serial3.write(0X54);//correction mode
  
  delay(4000);
  Serial3.write(0XA5);
  Serial3.write(0X51);
}

void loop() 
{  
serialEvent();
Serial.print(Roll);
Serial.print(" ");                 
Serial.print(Pitch);
Serial.print(" ");                 
Serial.println(Yaw);
//delay(1000);
}

void serialEvent() {

    Serial3.write(0XA5);
  Serial3.write(0X51);//send it for each read
while (Serial3.available()) {   
Re_buf[counter]=(unsigned char)Serial3.read();
if(counter==0&&Re_buf[0]!=0xAA) return;       
counter++;       
if(counter==8)               
{   
  counter=0;                 
  if(Re_buf[0]==0xAA && Re_buf[7]==0x55)  // data package is correct     
    {         
     Yaw=(int16_t)(Re_buf[1]<<8|Re_buf[2])/100.00;   
     Pitch=(int16_t)(Re_buf[3]<<8|Re_buf[4])/100.00;
     Roll=(int16_t)(Re_buf[5]<<8|Re_buf[6])/100.00;
    } 
delay(100);        
} 
}
}
