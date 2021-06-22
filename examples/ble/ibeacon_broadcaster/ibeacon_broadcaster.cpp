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

#define DEVICE_NAME         "Goto IoT iBeacon ESP32 001"
#define BEACON_UUID         "8ec76ea3-6668-48da-9866-75be8bc86f4d"

/*==================[internal data declaration]==============================*/

RTC_DATA_ATTR static uint32_t BootCount;
BLEAdvertising *BleAdvertising;

/*==================[internal functions declaration]=========================*/

void App_Init(void);
void App_Loop(void);

/*==================[internal data definition]===============================*/

/*==================[external data definition]===============================*/

/*==================[internal functions definition]==========================*/

void Ble_SetIBeaconAdvertising(){
    // creates iBeacon broadcaster
    BLEBeacon iBeacon = BLEBeacon();
    // fake Apple 0x004C LSB (ENDIAN_CHANGE_U16!)
    iBeacon.setManufacturerId(0x4C00);
    iBeacon.setProximityUUID(BLEUUID(BEACON_UUID));
    iBeacon.setMajor((BootCount & 0xFFFF0000) >> 16);
    iBeacon.setMinor(BootCount & 0xFFFF);
    // iBeacon.setSignalPower(-58);
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
    /** Advertising mode. Can be one of following constants:
     *  - BLE_GAP_CONN_MODE_NON (non-connectable; 3.C.9.3.2).
     *  - BLE_GAP_CONN_MODE_DIR (directed-connectable; 3.C.9.3.3).
     *  - BLE_GAP_CONN_MODE_UND (undirected-connectable; 3.C.9.3.4).
     */
    BleAdvertising->setAdvertisementType(BLE_GAP_CONN_MODE_NON);
}

void App_Init(){
    // Configure serial port at 115200 baudrios
    Serial.begin(SERIAL_BAURDATE);
    // Configure pins of buttons and leds
    pinMode(LED_ONBOARD, OUTPUT);
    // print informative message to serial console
    Serial.println("\n\r======================================\n\r");
    Serial.println("\n\rWelcome to BLE iBeacon Broadcaster - www.gotoiot.com");
    Serial.printf("Device has sent its iBeacon package %d times\n\r", BootCount++);
    // Create the BLE Device
    BLEDevice::init(DEVICE_NAME);
    BleAdvertising = BLEDevice::getAdvertising();
    Ble_SetIBeaconAdvertising();
    // Start advertising
    BleAdvertising->start();
    Serial.println("Starting to advertise iBeacon package");
    delay(ADVERTISING_DELAY);
    BleAdvertising->stop();
    Serial.printf("Stopping to advertise iBeacon package");
    Serial.printf("Entering in deep sleep mode for %d seconds", DEEP_SLEEP_SECONDS);
    Serial.println("\n\n\r======================================\n\r");
    Serial.println("\n\rESP32 Bootloader data\n\r");
    esp_deep_sleep(1000000LL * DEEP_SLEEP_SECONDS);
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