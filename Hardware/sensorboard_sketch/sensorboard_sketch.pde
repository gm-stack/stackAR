#include <Wire.h>

#define HMC5883_WriteAddress 0x1E //  i.e 0x3C >> 1
#define HMC5883_ModeRegisterAddress 0x02
#define HMC5883_ContinuousModeCommand 0x00
#define HMC5883_DataOutputXMSBAddress  0x03

#define regb 0x01
#define regbdata 0x40 //+- 4 Gauss
int outputData[6];
int magX, magY, magZ, i;

#define MMA7660addr   0x4c
#define MMA7660_X     0x00
#define MMA7660_Y     0x01
#define MMA7660_Z     0x02
#define MMA7660_TILT  0x03
#define MMA7660_SRST  0x04
#define MMA7660_SPCNT 0x05
#define MMA7660_INTSU 0x06
#define MMA7660_MODE  0x07
#define MMA7660_SR    0x08
#define MMA7660_PDET  0x09
#define MMA7660_PD    0x0A

unsigned char val[3];
int accX, accY, accZ;

struct dataSt {
  int magX;
  int magY;
  int magZ;
  int accX;
  int accY;
  int accZ;
} dataStr;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  
  Wire.beginTransmission(HMC5883_WriteAddress);
  Wire.send(regb);
  Wire.send(regbdata);
  Wire.endTransmission();
  delay(10);
  
  Wire.begin();
  Wire.beginTransmission( MMA7660addr);
  Wire.send(MMA7660_MODE);   
  Wire.send(0x00);
  Wire.endTransmission();
 
  Wire.beginTransmission( MMA7660addr);
  Wire.send(MMA7660_SR);   
  Wire.send(0x01);  //   Samples/Second Active and Auto-Sleep Mode
  Wire.endTransmission();
 
  Wire.beginTransmission( MMA7660addr);
  Wire.send(MMA7660_MODE);   
  Wire.send(0x01);//active mode
  Wire.endTransmission();
  
  while (Serial.read() == -1) {
  }
}

dataSt ret;
unsigned char ret2[12];
long nextTime;

#define frametime 50

void loop() {
    nextTime = millis() + frametime;
    Wire.beginTransmission(HMC5883_WriteAddress); //Initiate a transmission with HMC5883 (Write address).
    Wire.send(HMC5883_ModeRegisterAddress);       //Place the Mode Register Address in send-buffer.
    Wire.send(HMC5883_ContinuousModeCommand);     //Place the command for Continuous operation Mode in send-buffer.
    Wire.endTransmission();                       //Send the send-buffer to HMC5883 and end the I2C transmission.

    
    Wire.beginTransmission(HMC5883_WriteAddress);  //Initiate a transmission with HMC5883 (Write address).
    Wire.requestFrom(HMC5883_WriteAddress,6);      //Request 6 bytes of data from the address specified.
    
    if(6 <= Wire.available()) // If the number of bytes available for reading be <=6.
    {
        for(i=0;i<6;i++)
        {
            outputData[i]=Wire.receive();  //Store the data in outputData buffer
        }
    }
    
    ret.magX=outputData[0] << 8 | outputData[1]; //Combine MSB and LSB of X Data output register
    ret.magY=outputData[2] << 8 | outputData[3]; //Combine MSB and LSB of Z Data output register
    ret.magZ=outputData[4] << 8 | outputData[5]; //Combine MSB and LSB of Y Data output register
    
    i = 0;
    val[0] = val[1] = val[2] = 64;
    
    Wire.requestFrom(MMA7660addr,3);
    while (Wire.available()) {
      if (i < 3) {
        while (val[i] > 63) {
          val[i] = Wire.receive();
        }
        i++;
      }
    }
    
   ret.accX = ((val[0]<<2))/4;
   ret.accY = ((val[1]<<2))/4;
   ret.accZ = ((val[2]<<2))/4;
   
    memcpy(ret2,&ret,12);
    
    Serial.write(0xFF);
    Serial.write(ret2,12);
    Serial.write(0xFE);
    while (millis() < nextTime) {}; // wait until we are meant to push the next frame... or just skip ahead if we're late
}
