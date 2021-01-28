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

/*==================[macros and definitions]=================================*/

// APPLICATION SETTINGS
#define LED_ONBOARD                 2
#define INIT_DELAY                  3000
#define SERIAL_BAURDATE             115200
#define WIFI_CONNECTION_DELAY       500
#define MQTT_RETRY_CONNECTION_DELAY 5000
#define BLINK_TIME                  100
#define DEFAULT_PUBLISH_TIME        5000
#define MIN_PUBLISH_TIME            1000
#define MAX_PUBLISH_TIME            10000

/*==================[internal data declaration]==============================*/

// Client to establish WiFi connection
WiFiClient WifiClient;
// Client MQTT, needs a WiFi connection
PubSubClient MqttClient(WifiClient);
// Variable to change report time
static uint32_t PublishTime = DEFAULT_PUBLISH_TIME;

/*==================[internal functions declaration]=========================*/

void Gpio_BlinkLed           (uint8_t led, uint32_t milliseconds);
void Wifi_EstablishConnection(void);
void Mqtt_ConnectToBroker    (void);
void Mqtt_PublishTopic       (String topic, String payload);
void Mqtt_SubscribeCallback  (char* topic, byte* payload, unsigned int length);
void App_Init                (void);
void App_Loop                (void);

/*==================[internal data definition]===============================*/

// Device indentification
const String DEVICE_ID           = "mqtt-client-001";
// Wifi settings
const String WIFI_SSID           = "USER_WIFI_SSID";
const String WIFI_PASS           = "USER_WIFI_PASSWORD";
// Mqtt server settings
const String MQTT_SERVER         = "MQTT_HOST_IP_ADDRESS";
const int    MQTT_PORT           = 1883;
const String MQTT_USER           = "";
const String MQTT_PASS           = "";
// Mqtt message settings
const String MQTT_TOPIC_INIT     = DEVICE_ID + "/up";
const String MQTT_TOPIC_PRESSURE = DEVICE_ID + "/pressure";
const String MQTT_TOPIC_CONFIG   = DEVICE_ID + "/config/publish_time";

/*==================[external data definition]===============================*/

/*==================[internal functions definition]==========================*/

void Gpio_BlinkLed(uint8_t led, uint32_t milliseconds){
    // Blink on board led when topic is sended
    digitalWrite(led, true);
    delay(milliseconds);
    digitalWrite(led, false);
}

void Wifi_EstablishConnection(){
    // Print network SSID
    Serial.println();
    Serial.print("Connecting to ");
    Serial.print(WIFI_SSID);
    // Try to connect
    WiFi.begin(WIFI_SSID.c_str(), WIFI_PASS.c_str());
    // Wait until connection is established
    while (WiFi.status() != WL_CONNECTED) {
        delay(WIFI_CONNECTION_DELAY);
        Serial.print(".");
    }
    // Report IP address
    Serial.println("\n\rWiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}

void Mqtt_ConnectToBroker(){
    // Loop until we're reconnected
    while (!MqttClient.connected()) {
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        if (MqttClient.connect(DEVICE_ID.c_str())) {
            Serial.println("connected");
            // Subscribe to topic
            MqttClient.subscribe(MQTT_TOPIC_CONFIG.c_str());
            Serial.print("Subscribed to topic: ");
            Serial.println(MQTT_TOPIC_CONFIG.c_str());
        } else {
            Serial.print("failed, rc = ");
            Serial.print(MqttClient.state());
            Serial.println(". Try again in MQTT_RETRY_CONNECTION_TIME ms.");
            // Wait 5 seconds before retrying
            delay(MQTT_RETRY_CONNECTION_DELAY);
        }
    }
}

void Mqtt_PublishTopic(String topic, String payload){
    // Print in console the topic-payload that will be sent
    Serial.print("Sending MQTT Topic-Payload: ");
    Serial.print(topic);
    Serial.print(" -> ");
    Serial.println(payload);
    // Publish message
    MqttClient.publish( topic.c_str(), payload.c_str(), true );
}

void Mqtt_SubscribeCallback(char* topic, byte* payload, unsigned int length){
    if (strcmp(topic, MQTT_TOPIC_CONFIG.c_str()) == 0){
        // put null char to payload buffer
        payload[length] = '\0';
        // convert string value to int valie
        uint32_t publishTime = atoi((const char *)payload);
        // Check if value received is correct.
        if (publishTime >= MIN_PUBLISH_TIME && publishTime <= MAX_PUBLISH_TIME){
            Serial.print("Publish time will change to ");
            Serial.print((const char *)payload);
            Serial.print(" ms");
            // Change publish time
            PublishTime = publishTime;
        } else {
            Serial.print("Invalid publish time, must be between MIN_REPORT_TIME and MAX_REPORT_TIME ms.");
        }
        Serial.println();
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
    Serial.println("Welcome to Embedded MQTT Client - www.helloiot.net");
    // Set MQTT Server
    MqttClient.setServer(MQTT_SERVER.c_str(), MQTT_PORT);
    // Configure a callback to receive topics
    MqttClient.setCallback(Mqtt_SubscribeCallback);
    // Connect to WiFi
    Wifi_EstablishConnection();
    // Leave built in led on
    digitalWrite(LED_ONBOARD, false);
}

void App_Loop(){
    // Create a variable to publish topic
    static uint32_t tickCounter = 0;
    // Create a fake variable to send a pressure value
    static uint32_t fakePressureValue = 1000;
    // Check if MQTT client is not connected to server.
    if (!MqttClient.connected()) {
        // Try to connect with MQTT Server.
        Mqtt_ConnectToBroker();
    }
    // Loop for incoming messages.
    MqttClient.loop();
    // Use this variable to unblock the loop
    if (++tickCounter >= PublishTime){
        // Reset counter
        tickCounter = 0;
        // Array to send fake pressure value
        char pressureValueStr [6];
        // Convert int pressure value to str pressure vale
        itoa(++fakePressureValue, pressureValueStr, 10);
        // Send MQTT Topic
        Mqtt_PublishTopic(MQTT_TOPIC_PRESSURE, pressureValueStr);
        // Blink LED
        Gpio_BlinkLed(LED_ONBOARD, BLINK_TIME);
    }
    // delay 1 MS to start loop again
    delay(1);
}
    
/*==================[external functions definition]==========================*/

void setup(){
    App_Init();
}

void loop(){
    App_Loop();
}

/*==================[end of file]============================================*/
