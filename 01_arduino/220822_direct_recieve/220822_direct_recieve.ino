
float Roll,Pitch,Yaw;
//float Deg[3] = {Roll, Pitch, Yaw};
unsigned char Re_buf[8];
unsigned char counter = 0;
byte databyte;

void setup() {
  // put your setup code here, to run once:'
  Serial.begin(9600); //PC
  Serial3.begin(9600); //GY

  // set GY
  delay(4000);
  Serial3.write(0XA5);
  Serial3.write(0X54);//correction mode
  
  delay(4000);
  Serial3.write(0XA5);
  Serial3.write(0X51);
  //0X51:query mode, return directly to the angle value, to be sent each read, 0X52:Automatic mode,send a direct return angle, only initialization
}

void loop() {
  // put your main code here, to run repeatedly:
  serialEvent();

  Serial.print(" 1");
  Serial.print(Roll);
  Serial.print(" ");                 
  Serial.print(Pitch);
  Serial.print(" ");                 
  Serial.print(Yaw);

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
