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
#include "secrets.h"

/*==================[macros and definitions]=================================*/

// GENERAL BEHAVIOUR SETTINGS
#define INIT_DELAY          3000
#define SERIAL_BAURDATE     115200
#define LED_ONBOARD         2
#define BUTTON_ONBOARD      0
// APPLICATION SETTINGS
#define LED_DELAY           500
#define DEEP_SLEEP_SECONDS  10
#define ADVERTISING_DELAY   100
#define IBEACON_TX_POWER    0

/*==================[internal data declaration]==============================*/

RTC_DATA_ATTR static uint32_t BootCount;
RTC_DATA_ATTR static uint32_t BeaconMajor = IBEACON_DEFAULT_MAJOR;
RTC_DATA_ATTR static uint32_t BeaconMinor = IBEACON_DEFAULT_MINOR;
BLEAdvertising *BleAdvertising;

/*==================[internal functions declaration]=========================*/

void Core_DeepSleepDelay            (uint32_t delaySeconds);
void Serial_PrintSeparator          (void);
void Ble_SetDeviceAsIBeacon         (uint32_t major, uint32_t minor, uint32_t txPower);
void Ble_PerformAdvertisingCycle    (void);
void App_ShowWelcomeMessage         (void);
void App_ShowStopAdvertisingMessage (void);
void App_UpdateIBeaconData          (void);
void App_Init                       (void);
void App_Loop                       (void);

/*==================[internal data definition]===============================*/

/*==================[external data definition]===============================*/

/*==================[internal functions definition]==========================*/

void Core_DeepSleepDelay(uint32_t delaySeconds){
    esp_deep_sleep(1000000LL * delaySeconds);
}

void Serial_PrintSeparator(){
    Serial.print("\n\n\r======================================\n\n\r");
}

void Ble_SetDeviceAsIBeacon(uint32_t major, uint32_t minor, uint32_t txPower){
    BLEDevice::init(DEVICE_ID);
    BleAdvertising = BLEDevice::getAdvertising();
    // creates iBeacon broadcaster
    BLEBeacon iBeacon = BLEBeacon();
    iBeacon.setManufacturerId(IBEACON_MANUFACTURER_ID);
    iBeacon.setProximityUUID(BLEUUID(IBEACON_UUID));
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
        IBEACON_UUID, BeaconMajor, BeaconMinor, IBEACON_TX_POWER);
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
    if(!digitalRead(BUTTON_ONBOARD)){
        BeaconMajor = (BootCount & 0xFFFF0000) >> 16;
        BeaconMinor = BootCount & 0xFFFF;
        Serial.printf("Changing major value to '%d' and minor value to '%d'\n\r", BeaconMajor, BeaconMinor);
        delay(200);
    }
}

void App_Init(){
    Serial.begin(SERIAL_BAURDATE);
    pinMode(LED_ONBOARD, OUTPUT);
    pinMode(BUTTON_ONBOARD, INPUT);
    App_ShowWelcomeMessage();
    App_UpdateIBeaconData();
    Ble_SetDeviceAsIBeacon(BeaconMajor, BeaconMinor, IBEACON_TX_POWER);
}

void App_Loop(){
    Ble_PerformAdvertisingCycle();
    App_ShowStopAdvertisingMessage();
    Core_DeepSleepDelay(DEEP_SLEEP_SECONDS);
}

/*==================[external functions definition]==========================*/

void setup(){
    App_Init();
}

void loop(){
    App_Loop();
}

/*==================[end of file]============================================*/