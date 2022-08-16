
// Connect RX of GY 25 to TX3 Arduino Mega and TX of GY 25 to RX3 Arduino Mega

float Roll,Pitch,Yaw;
//float Deg[3] = {Roll, Pitch, Yaw};
unsigned char Re_buf[8];
unsigned char counter = 0;

void setup()
{
  // PC
//  Serial.begin(9600);
  // GY
  Serial3.begin(9600);// SoftwareSerial can only support 9600 baud rate for GY 25 but Serial3 can support 115200 and 9600 both
  // Radio
  Serial1.begin(9600);

  // set GY
  delay(4000);
  Serial3.write(0XA5);
  Serial3.write(0X54);//correction mode
  delay(4000);
  Serial3.write(0XA5);
  Serial3.write(0X51);//0X51:query mode, return directly to the angle value, to be sent each read, 0X52:Automatic mode,send a direct return angle, only initialization
}

void loop() {
  serialEvent();
//  float Deg[3] = {Roll, Pitch, Yaw};
//  int i=0;
  
//  Serial.print(Roll);
//  Serial.print(" ");                 
//  Serial.print(Pitch);
//  Serial.print(" ");                 
//  Serial.println(Yaw);
  
  Serial1.print(" 1");
  Serial1.print(Roll);
  Serial1.print(" ");                 
  Serial1.print(Pitch);
  Serial1.print(" ");                 
  Serial1.print(Yaw);
//  Serial1.print("\n");
  
  delay(200);
}

void serialEvent() {
  Serial3.write(0XA5);
  Serial3.write(0X51);//send it for each read
  
  while (Serial3.available()) {   
    Re_buf[counter] = (unsigned char) Serial3.read();
    if (counter==0 && Re_buf[0] != 0xAA) return;
    counter++;
    if(counter==8)
    {
      counter=0;                 
      if(Re_buf[0] == 0xAA && Re_buf[7] == 0x55)  // data package is correct     
      {
        Yaw   = (int16_t)(Re_buf[1]<<8|Re_buf[2])/100.00;   
        Pitch = (int16_t)(Re_buf[3]<<8|Re_buf[4])/100.00;
        Roll  = (int16_t)(Re_buf[5]<<8|Re_buf[6])/100.00;
      }
      delay(100);
    }
  }
}
