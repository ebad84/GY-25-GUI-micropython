
float Roll,Pitch,Yaw;
//float Deg[3] = {Roll, Pitch, Yaw};
unsigned char Re_buf[8];
int counter = 0;
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



//  Serial.print(" 1");
//  Serial.print(Roll);
//  Serial.print(" ");                 
//  Serial.print(Pitch);
//  Serial.print(" ");                 
//  Serial.print(Yaw);
//  Serial.print("\n");

  delay(200);
}

void serialEvent() {
  Serial3.write(0XA5);
  Serial3.write(0X51);//send it for each read
  
  while (Serial3.available()) {
    Serial.println("========= Available =========");
    Re_buf[counter] = (unsigned char) Serial3.read();
    Serial.println(Re_buf[0]);
    Serial.println(Re_buf[1]);
    Serial.println(Re_buf[2]);
    Serial.println(Re_buf[3]);
    Serial.println(Re_buf[4]);
    Serial.println(Re_buf[5]);
    Serial.println(Re_buf[6]);
    Serial.println(Re_buf[7]);
    
    if (counter==0 && Re_buf[0] != 0xAA) {
        return;
      };
    
    counter++;
//    Serial.print(counter);
    
    if(counter==8)
    {
      Serial.print("counter: ");
      Serial.println(counter);
      counter=0;                 
      if(Re_buf[0] == 0xAA && Re_buf[7] == 0x55)  // data package is correct     
      {
        Serial.print("======== Value ========");
        Yaw   = (int16_t)(Re_buf[1]<<8|Re_buf[2])/100.00;
        Serial.print("Yaw: ");
        Serial.println(Yaw);   
        Pitch = (int16_t)(Re_buf[3]<<8|Re_buf[4])/100.00;
        Serial.print("Pitch: ");
        Serial.println(Pitch);
        Roll  = (int16_t)(Re_buf[5]<<8|Re_buf[6])/100.00;
        Serial.print("Roll: ");
        Serial.println(Roll);
      }
      delay(100);
    }
  }
}
