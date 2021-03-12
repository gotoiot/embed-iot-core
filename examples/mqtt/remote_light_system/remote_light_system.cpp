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

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "secrets.h"

/*==================[macros and definitions]=================================*/

// GENERAL BEHAVIOUR SETTINGS
#define INIT_DELAY                  3000
#define WIFI_CONNECTION_DELAY       500
#define MQTT_RETRY_CONNECTION_DELAY 5000
// HARDWARE SETTINGS
#define SERIAL_BAURDATE             115200
#define LED_ONBOARD                 2
// APPLICATION SETTINGS
#define BLINK_TIME                  100
#define DEFAULT_PUBLISH_TIME        5000
#define MIN_PUBLISH_TIME            1000
#define MAX_PUBLISH_TIME            10000
#define WILL_RETAIN_MESSAGE         false
#define WILL_QOS                    2
// MQTT TOPICS/DATA
#define TOPIC_PUB_UP                "/up"
#define TOPIC_PUB_DOWN              "/down"
#define TOPIC_PUB_STATUS            "/" DEVICE_ID "/status"
#define TOPIC_SUB_STATUS            "/status/" DEVICE_ID
#define TOPIC_SUB_LED               "/led/" DEVICE_ID
#define TOPIC_SUB_LED_STATUS        "/led/status/" DEVICE_ID 
#define TOPIC_PUB_LED_STATUS        "/" DEVICE_ID "/led/status/" 
#define TOPIC_SUB_ALL_LED           "/all/led"
#define TOPIC_SUB_ALL_LED_STATUS    "/all/led/status"

/*==================[internal data declaration]==============================*/

// Client to establish WiFi connection
WiFiClient WifiClient;
// Client MQTT, needs a WiFi connection
PubSubClient MqttClient(WifiClient);
// Variable to change report time
static uint32_t PublishTime;

/*==================[internal functions declaration]=========================*/

void   Gpio_BlinkOutput           (uint8_t output, uint32_t milliseconds);
void   Wifi_EstablishConnection   (void);
char * Wifi_GetIpAsString         (void);
void   Mqtt_ConnectToBroker       (void);
void   Mqtt_PublishTopic          (const char * topic, const char * payload);
void   Mqtt_SubscribeCallback     (char* topic, byte* payload, unsigned int length);
char * App_GetDeviceStatusAsJson  (void);
char * App_GetLedStatusAsJson (void);
char * App_GetDeviceIdAsJson      (void);
void   App_Init                   (void);
void   App_Loop                   (void);

/*==================[internal data definition]===============================*/

/*==================[external data definition]===============================*/

/*==================[internal functions definition]==========================*/

void Gpio_BlinkOutput(uint8_t output, uint32_t milliseconds){
    digitalWrite(output, true);
    delay(milliseconds);
    digitalWrite(output, false);
}

void Wifi_EstablishConnection(){
    // Print network SSID
    Serial.printf("\n\rTrying connection to Wifi SSID '%s'", WIFI_SSID);
    // Try to connect
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    // Wait until connection is established
    while (WiFi.status() != WL_CONNECTED) {
        delay(WIFI_CONNECTION_DELAY);
        Serial.print(".");
    }
    // Report IP address
    Serial.printf("\n\rWifi connected. Assigned device IP: '%s'", Wifi_GetIpAsString());
}

char * Wifi_GetIpAsString(){
    static char ipArray[26];
    IPAddress ipNumber = WiFi.localIP();
    sprintf(ipArray, "%d.%d.%d.%d", 
        ipNumber[0], ipNumber[1], ipNumber[2], ipNumber[3]);
    return ipArray;
}

void Mqtt_ConnectToBroker(){
    // Loop until we're reconnected
    while (!MqttClient.connected()) {
        Serial.printf("\n\rTrying connection to MQTT broker '%s:%d'", MQTT_HOST, MQTT_PORT);
        // Attempt to connect
        bool connectionStatus = MqttClient.connect(
            DEVICE_ID, MQTT_USER, MQTT_PASS, TOPIC_PUB_DOWN, 
            WILL_QOS, WILL_RETAIN_MESSAGE, App_GetDeviceIdAsJson()
            );
        // Attempt to connect
        if (connectionStatus){
            Serial.print("\n\rConnected to MQTT broker successfully");
            // Subscribe to topic config
            MqttClient.subscribe(TOPIC_SUB_LED);
            Serial.printf("\n\rSubscribed to topic: %s", TOPIC_SUB_LED);
            // Subscribe to topic to report status
            MqttClient.subscribe(TOPIC_SUB_STATUS);
            Serial.printf("\n\rSubscribed to topic: %s", TOPIC_SUB_STATUS);
            // Subscribe to topic to report LED status individually
            MqttClient.subscribe(TOPIC_SUB_LED_STATUS);
            Serial.printf("\n\rSubscribed to topic: %s", TOPIC_SUB_LED_STATUS);
            // Subscribe to topic to control all led at same time
            MqttClient.subscribe(TOPIC_SUB_ALL_LED);
            Serial.printf("\n\rSubscribed to topic: %s", TOPIC_SUB_ALL_LED);
            // Subscribe to topic to report all status at same time
            MqttClient.subscribe(TOPIC_SUB_ALL_LED_STATUS);
            Serial.printf("\n\rSubscribed to topic: %s", TOPIC_SUB_ALL_LED_STATUS);
            // Advice that device is up and running
            Mqtt_PublishTopic(TOPIC_PUB_UP, App_GetDeviceStatusAsJson());
        } else {
            Serial.printf("\n\rFailed to connect to broker (Error code: %d). Retrying in %d ms", 
                MqttClient.state(), MQTT_RETRY_CONNECTION_DELAY);
            delay(MQTT_RETRY_CONNECTION_DELAY);
        }
    }
}

void Mqtt_PublishTopic(const char * topic, const char * payload){
    Serial.printf("\n\rSending MQTT Topic '%s' -> '%s'", topic, payload);
    MqttClient.publish(topic, payload, true);
}

void Mqtt_SubscribeCallback(char* topic, byte* payload, unsigned int length){
    // At first check if topic arrived is some of expected topics
    if ((strcmp(topic, TOPIC_SUB_LED) == 0) || 
        (strcmp(topic, TOPIC_SUB_ALL_LED) == 0)){
        // put null char to payload buffer
        payload[length] = '\0';
        // Compare the topic payload to expected values
        if( (strcmp((char *)payload, "on") == 0) || (strcmp((char *)payload, "off") == 0) ){
            bool status = false;
            // set the LED status depending on the payload
            if(strcmp((char *)payload, "on") == 0){
                status = true;
            } 
            digitalWrite(LED_ONBOARD, status);
            // Report the action in console
            Serial.print("Changing the LED status to: ");
            Serial.println(status);
        } else {
            Serial.println("Invalid LED status. It must be 'on' or 'off'.");
        }
    } else if ((strcmp(topic, TOPIC_SUB_LED_STATUS) == 0) || 
        (strcmp(topic, TOPIC_SUB_ALL_LED_STATUS) == 0)){
        bool ledStatus = digitalRead(LED_ONBOARD);
        // Publish the state of the onboard LED
        Mqtt_PublishTopic(TOPIC_PUB_LED_STATUS, App_GetLedStatusAsJson());
    } else if (strcmp(topic, TOPIC_SUB_STATUS) == 0){
        Serial.println("Sending device status");
        Mqtt_PublishTopic(TOPIC_PUB_STATUS, App_GetDeviceStatusAsJson());
    } else {
        Serial.println("Unknown topic received!");
    }
}

void App_Init(){
    // wait a moment before start
    delay(INIT_DELAY);
    // Configure serial port at 115200 baudrios
    Serial.begin(SERIAL_BAURDATE);
    // Configure pins of buttons and leds
    pinMode(LED_ONBOARD, OUTPUT);
    // print to console Init message
    Serial.println("\n\n\rWelcome to Remote light system - www.gotoiot.com");
    // Leave built in led on
    digitalWrite(LED_ONBOARD, false);
    // Set MQTT Server
    MqttClient.setServer(MQTT_HOST, MQTT_PORT);
    // Configure a callback to receive topics
    MqttClient.setCallback(Mqtt_SubscribeCallback);
    // Connect to WiFi
    Wifi_EstablishConnection();
    // Set a default publish time to send topics
    PublishTime = DEFAULT_PUBLISH_TIME;
}

char * App_GetLedStatusAsJson(){
    StaticJsonDocument<100> doc;
    static char jsonBuffer[100];
    bool ledStatus = digitalRead(LED_ONBOARD);
    doc["status"] = ledStatus ? "on": "off"
    doc["time"] = millis();
    serializeJson(doc, jsonBuffer);
    return jsonBuffer;
}

char * App_GetDeviceStatusAsJson(){
    StaticJsonDocument<100> doc;
    static char jsonBuffer[100];
    doc["device_id"] = DEVICE_ID;
    doc["ip"] = Wifi_GetIpAsString();
    doc["status"] = "running";
    serializeJson(doc, jsonBuffer);
    return jsonBuffer;
}

char * App_GetDeviceIdAsJson(){
    StaticJsonDocument<100> doc;
    static char jsonBuffer[100];
    doc["device_id"] = DEVICE_ID;
    serializeJson(doc, jsonBuffer);
    return jsonBuffer;
}

void App_Loop(){
    // Check if MQTT client is not connected to server.
    if (!MqttClient.connected()) {
        // Try to connect with MQTT Server.
        Mqtt_ConnectToBroker();
    }
    // Loop for incoming messages.
    MqttClient.loop();
}
    
/*==================[external functions definition]==========================*/

void setup(){
    App_Init();
}

void loop(){
    App_Loop();
}

/*==================[end of file]============================================*/
