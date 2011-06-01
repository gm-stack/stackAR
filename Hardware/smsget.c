#import <stdio.h>
#include <mach/mach.h>
#include <IOKit/IOKitLib.h>
#include <CoreFoundation/CoreFoundation.h>

static io_connect_t dataPort = 0;

typedef struct {
    char x;
    char y;
    char z;
    // filler space to make size of the structure at least 60 bytes
    char pad[57];
} MotionSensorData_t;

int main() {
    kern_return_t status = sms_initialize();
    printf("status = %i\n",status);
    MotionSensorData_t msd;
    status = sms_getOrientation(&msd);
    printf("status = %i\n",status);
    printf("%i,%i,%i\n",msd.x,msd.y,msd.z);
}

kern_return_t
sms_initialize(void)
{
    kern_return_t   kr;
    CFDictionaryRef classToMatch;
    io_service_t    service;
   
    // create a matching dictionary given the class name, which,
    // depends on hardware (e.g. "IOI2CMotionSensor" or "PMUMotionSensor")
    classToMatch = IOServiceMatching("SMCMotionSensor");
   
    // look up the IOService object (must already be registered)
    service = IOServiceGetMatchingService(kIOMasterPortDefault, classToMatch);
    if (!service)
        return KERN_FAILURE;
   
    // create a connection to the IOService object
    kr = IOServiceOpen(service,          // the IOService object
                       mach_task_self(), // the task requesting the connection
                       0,                // type of connection 
                       &dataPort);       // connection handle
   
    IOObjectRelease(service);
   
    return kr;
}


static const int getOrientationUC_methodID = 21;

kern_return_t sms_getOrientation(MotionSensorData_t *data)
{
    kern_return_t      kr;
    IOByteCount        size = 60;
    MotionSensorData_t unused_struct_in = { 0 };
    
    kr = IOConnectMethodStructureIStructureO(dataPort,
                                             getOrientationUC_methodID,
                                             size,
                                             &size,
                                             &unused_struct_in,
                                             data);
    return kr;
}