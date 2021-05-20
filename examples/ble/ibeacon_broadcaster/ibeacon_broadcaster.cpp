/* MIT License

Copyright (c) 2021 Agustin Bassi (github.com/agustinBassi)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.*/

/*==================[inclusions]=============================================*/

#include <Arduino.h>
#include <sys/time.h>

#include "BLEDevice.h"
#include "BLEUtils.h"
#include "BLEBeacon.h"
#include "esp_sleep.h"

/*==================[macros and definitions]=================================*/

// GENERAL BEHAVIOUR SETTINGS
#define INIT_DELAY          3000
#define SERIAL_BAURDATE     115200
#define LED_ONBOARD         2
// APPLICATION SETTINGS
#define LED_DELAY           500
#define DEEP_SLEEP_SECONDS  10
#define ADVERTISING_DELAY   100

// #define BEACON_UUID         "8ec76ea3-6668-48da-9866-75be8bc86f4d"
#define BEACON_UUID         "ffeeccdd-bbaa-9988-7766-554433221100"

/*==================[internal data declaration]==============================*/

RTC_DATA_ATTR static uint32_t BootCount; 
BLEAdvertising *BleAdvertising;

/*==================[internal functions declaration]=========================*/

void App_Init (void);
void App_Loop (void);

/*==================[internal data definition]===============================*/

/*==================[external data definition]===============================*/

/*==================[internal functions definition]==========================*/

void Ble_SetIBeaconAdvertising(){
    // creates iBeacon broadcaster
    BLEBeacon iBeacon = BLEBeacon();
    iBeacon.setManufacturerId(0x4C00);
    iBeacon.setProximityUUID(BLEUUID(BEACON_UUID));
    iBeacon.setMajor((BootCount & 0xFFFF0000) >> 16);
    iBeacon.setMinor(BootCount & 0xFFFF);
    iBeacon.setSignalPower(-58);
    BLEAdvertisementData advertisementData = BLEAdvertisementData();
    BLEAdvertisementData scanResponseData = BLEAdvertisementData();
    // BR_EDR_NOT_SUPPORTED 0x04
    advertisementData.setFlags(0x04); 
    // prepares advertising data
    std::string strServiceData = "";
    strServiceData += (char)26;
    strServiceData += (char)0xFF;
    strServiceData += iBeacon.getData();
    advertisementData.addData(strServiceData);
    // set BLE advertising accordingly
    BleAdvertising->setAdvertisementData(advertisementData);
    BleAdvertising->setScanResponseData(scanResponseData);
    BleAdvertising->setAdvertisementType(ADV_TYPE_NONCONN_IND);
}

void App_Init(){
    // Configure serial port at 115200 baudrios
    Serial.begin(SERIAL_BAURDATE);
    // Configure pins of buttons and leds
    pinMode(LED_ONBOARD, OUTPUT);
    // print informative message to serial console
    gettimeofday(&NowTime, NULL);
    Serial.println("\n\n\rWelcome to BLE iBeacon Broadcaster - www.gotoiot.com");
    Serial.printf("Device has sent its iBeacon package %d times\n\r", BootCount++);
    // Create the BLE Device
    BLEDevice::init("Goto IoT ESP32 iBeacon");
    BleAdvertising = BLEDevice::getAdvertising();
    Ble_SetIBeaconAdvertising();
    // Start advertising
    BleAdvertising->start();
    Serial.println("Starting to advertise iBeacon package");
    delay(ADVERTISING_DELAY);
    BleAdvertising->stop();
    Serial.printf("Stopping to advertise iBeacon package");
    esp_deep_sleep(1000000LL * DEEP_SLEEP_SECONDS);
    Serial.printf("Entering in deep sleep mode for %d seconds", DEEP_SLEEP_SECONDS);
}

void App_Loop(){
    // nothing to do
}
    
/*==================[external functions definition]==========================*/

void setup(){
    App_Init();
}

void loop(){
    App_Loop();
}

/*==================[end of file]============================================*/
