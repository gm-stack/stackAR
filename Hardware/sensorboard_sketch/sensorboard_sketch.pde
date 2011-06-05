#include <Wire.h>

#define ACCEL
#define COMPASS
#define GYRO

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

#define WHO	0x00
#define	SMPL	0x15
#define DLPF	0x16
#define INT_C	0x17
#define INT_S	0x1A
#define	TMP_H	0x1B
#define	TMP_L	0x1C
#define	GX_H	0x1D
#define	GX_L	0x1E
#define	GY_H	0x1F
#define	GY_L	0x20
#define GZ_H	0x21
#define GZ_L	0x22
#define PWR_M	0x3E
#define GYRO_ADDRESS 0x68


char ITG3200Readbyte(unsigned char address)
{
   char data;
 
	  Wire.beginTransmission(GYRO_ADDRESS);
	  Wire.send((address));
	  Wire.endTransmission();
	  Wire.requestFrom(GYRO_ADDRESS,1);
	  if (Wire.available()>0)
	    {
	    data = Wire.receive();
	    }
	    return data;
 
 
	   Wire.endTransmission();
}
 
char ITG3200Read(unsigned char addressh,unsigned char addressl)
{
   char data;
 
	  Wire.beginTransmission(GYRO_ADDRESS);
	  Wire.send((addressh));
	    Wire.endTransmission();
	  Wire.requestFrom(GYRO_ADDRESS,1);
	  if (Wire.available()>0)
	    {
	    data = Wire.receive();
	    }
	  Wire.beginTransmission(GYRO_ADDRESS);
	    Wire.send((addressl));
	    Wire.endTransmission();
	    if (Wire.available()>0)
	    {
	    data |= Wire.receive()<<8;
	    }
	    return data;
 
 
//	   Wire.endTransmission();
}
 
 
 
void Gyro_Init(void)
{
  Wire.beginTransmission(GYRO_ADDRESS);
  Wire.send(0x3E);
  Wire.send(0x80);  //send a reset to the device
  Wire.endTransmission(); //end transmission
 
 
  Wire.beginTransmission(GYRO_ADDRESS);
  Wire.send(0x15);
  Wire.send(0x00);   //sample rate divider
  Wire.endTransmission(); //end transmission
 
  Wire.beginTransmission(GYRO_ADDRESS);
  Wire.send(0x16);
  Wire.send(0x18); // ±2000 degrees/s (default value)
  Wire.endTransmission(); //end transmission
 
//  Wire.beginTransmission(GYRO_ADDRESS);
//  Wire.send(0x17);
//  Wire.send(0x05);   // enable send raw values
//  Wire.endTransmission(); //end transmission
 
//  Wire.beginTransmission(GYRO_ADDRESS);
//  Wire.send(0x3E);
//  Wire.send(0x00);
//  Wire.endTransmission(); //end transmission
}


unsigned char val[3];
int accX, accY, accZ;

struct dataSt {
  #ifdef COMPASS
  int magX;
  int magY;
  int magZ;
  #endif

 #ifdef ACCEL
  int accX;
  int accY;
  int accZ;
  #endif
  
  #ifdef GYRO
  int gyrX;
  int gyrY;
  int gyrZ;
  #endif
} dataStr;

void setup() {
  Serial.begin(115200);

  Wire.begin();
  
  Gyro_Init();
  
  Wire.beginTransmission(HMC5883_WriteAddress);
  Wire.send(regb);
  Wire.send(regbdata);
  Wire.endTransmission();
  delay(10);
  
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
unsigned char ret2[18];
long nextTime;

#define frametime 20

void loop() {
    nextTime = millis() + frametime;
  
  ret.gyrX = ITG3200Read(GX_H,GX_L);
  ret.gyrY = ITG3200Read(GY_H,GY_L);
  ret.gyrZ = ITG3200Read(GZ_H,GZ_L);
    
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
   
    memcpy(ret2,&ret,18);
    
    Serial.write(0xFF);
    Serial.write(ret2,18);
    Serial.write(0xFE);
    while (millis() < nextTime) {}; // wait until we are meant to push the next frame... or just skip ahead if we're late
}
