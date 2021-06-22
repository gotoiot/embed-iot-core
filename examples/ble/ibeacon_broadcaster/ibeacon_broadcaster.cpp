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

#include "Arduino.h"
#include "sys/time.h"
#include "NimBLEDevice.h"
#include "NimBLEBeacon.h"
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
#define BLE_TX_POWER        0
#define DEVICE_NAME         "Goto IoT iBeacon ESP32 001"
#define BEACON_UUID         "8ec76ea3-6668-48da-9866-75be8bc86f4d"

/*==================[internal data declaration]==============================*/

RTC_DATA_ATTR static uint32_t BootCount;
BLEAdvertising *BleAdvertising;
static uint32_t BeaconMajor = 0;
static uint32_t BeaconMinor = 0;

/*==================[internal functions declaration]=========================*/

void App_Init(void);
void App_Loop(void);

/*==================[internal data definition]===============================*/

/*==================[external data definition]===============================*/

/*==================[internal functions definition]==========================*/

void Core_SetEsp32ToDeepSleep(){
    esp_deep_sleep(1000000LL * DEEP_SLEEP_SECONDS);
}

void Serial_PrintSeparator(){
    Serial.print("\n\n\r======================================\n\n\r");
}

void Ble_SetDeviceAsIBeacon(uint32_t major, uint32_t minor, uint32_t txPower){
    BLEDevice::init(DEVICE_NAME);
    BleAdvertising = BLEDevice::getAdvertising();
    // creates iBeacon broadcaster
    BLEBeacon iBeacon = BLEBeacon();
    // fake Apple 0x004C LSB (ENDIAN_CHANGE_U16!)
    iBeacon.setManufacturerId(0x4C00);
    iBeacon.setProximityUUID(BLEUUID(BEACON_UUID));
    iBeacon.setMajor(major);
    iBeacon.setMinor(minor);
    iBeacon.setSignalPower(txPower);
    BLEAdvertisementData advertisementData = BLEAdvertisementData();
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
    BleAdvertising->setAdvertisementType(BLE_GAP_CONN_MODE_NON);
}

void Ble_PerformAdvertisingCycle(){
    Serial.printf("iBeacon data: {\"uuid\": %s, \"major\": %d, \"minor\": %d, \"tx_power\": %d}\n\r",
        BEACON_UUID, BeaconMajor, BeaconMinor, BLE_TX_POWER);
    BleAdvertising->start();
    delay(ADVERTISING_DELAY);
    BleAdvertising->stop();
}

void App_ShowWelcomeMessage(){
    Serial_PrintSeparator();
    Serial.printf("Welcome to BLE iBeacon Broadcaster - www.gotoiot.com\n\r");
    Serial.printf("iBeacon device has sent packages for %d times\n\r", BootCount);
}

void App_ShowStopAdvertisingMessage(){
    Serial.printf("Stopping to advertise iBeacon package\n\r");
    Serial.printf("Entering in deep sleep mode for %d seconds\n\r", DEEP_SLEEP_SECONDS);
    Serial_PrintSeparator();
}

void App_UpdateIBeaconData(){
    BootCount += 1;
    BeaconMajor = (BootCount & 0xFFFF0000) >> 16;
    BeaconMinor = BootCount & 0xFFFF;
}

void App_Init(){
    Serial.begin(SERIAL_BAURDATE);
    pinMode(LED_ONBOARD, OUTPUT);
    App_ShowWelcomeMessage();
    App_UpdateIBeaconData();
    Ble_SetDeviceAsIBeacon(BeaconMajor, BeaconMinor, BLE_TX_POWER);
}


void App_Loop(){
    Ble_PerformAdvertisingCycle();
    App_ShowStopAdvertisingMessage();
    Core_SetEsp32ToDeepSleep();
}

/*==================[external functions definition]==========================*/

void setup(){
    App_Init();
}

void loop(){
    App_Loop();
}

/*==================[end of file]============================================*/