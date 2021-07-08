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

/*===================[inclusions]============================================*/

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <coap-simple.h>
#include "secrets.h"

/*==================[macros and definitions]=================================*/

// APPLICATION SETTINGS
#define LED_ONBOARD                         2
#define BUTTON_ONBOARD                      0
#define INIT_DELAY                          3000
#define SERIAL_BAURDATE                     115200
#define WIFI_CONNECTION_DELAY               500
// COAP SERVER SETTINGS
#define COAP_SERVER_PORT                    5683
// COAP RESOURCES SETTINGS
#define COAP_RESOURCE_LIGHT                 "light"
#define COAP_RESOURCE_BUTTON                "button"
#define COAP_RESOURCE_WELL_KNOWN            ".well-known/core"
#define LIGHT_OFF_REQUEST_PAYLOAD           "{\"light\":false}"
#define LIGHT_ON_REQUEST_PAYLOAD            "{\"light\":true}"
#define LIGHT_OFF_RESPONSE_PAYLOAD          "{\"light\":false}"
#define LIGHT_ON_RESPONSE_PAYLOAD           "{\"light\":true}"
#define BUTTON_PRESSED_RESPONSE_PAYLOAD     "{\"button\":false}"
#define BUTTON_NOT_PRESSED_RESPONSE_PAYLOAD "{\"button\":true}"

/*==================[internal data declaration]==============================*/

WiFiUDP WiFiUdp;
Coap    Coap(WiFiUdp);

/*==================[external data definition]===============================*/

void   Wifi_EstablishConnection    (void);
char * Wifi_GetIpAsString          (void);
void   Coap_InitServer             (void);
void   Coap_LogPacketInfo          (CoapPacket &packet);
void   Coap_WellKnownCallback      (CoapPacket &packet, IPAddress ip, int port);
void   Coap_ResponseCallback       (CoapPacket &packet, IPAddress ip, int port);
void   Coap_LightResourceCallback  (CoapPacket &packet, IPAddress ip, int port);
void   Coap_ButtonResourceCallback (CoapPacket &packet, IPAddress ip, int port);
void   App_Init                    (void);
void   App_Loop                    (void);

/*==================[internal functions definition]==========================*/

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

void Coap_InitServer(void){
    // configure callback to light resource
    Serial.println("[Coap_InitServer] - Setup Callback Light");
    Coap.server(Coap_LightResourceCallback, COAP_RESOURCE_LIGHT);
    // configure callback to button resource
    Serial.println("[Coap_InitServer] - Setup Callback Button");
    Coap.server(Coap_ButtonResourceCallback, COAP_RESOURCE_BUTTON);
    // configure callback for discovery the server resources
    Serial.println("[Coap_InitServer] - Setup Callback Well known");
    Coap.server(Coap_WellKnownCallback, COAP_RESOURCE_WELL_KNOWN);
    // client response callback single callback
    Serial.println("[Coap_InitServer] - Setup Response Callback");
    Coap.response(Coap_ResponseCallback);
    // start coap server/client
    Coap.start(COAP_SERVER_PORT);
}

void Coap_LogPacketInfo(CoapPacket &packet){
    // Start of log info
    Serial.println("\n\n\r==================================================");
    Serial.println("Coap_LogPacketInfo");
    Serial.println("------------------\n\r");
    // Show message method
    Serial.print(" - Method:         ");
    if (packet.code == COAP_GET){
        Serial.println("COAP_GET");
    } else if (packet.code == COAP_POST){
        Serial.println("COAP_POST");
    } else if (packet.code == COAP_PUT){
        Serial.println("COAP_PUT");
    } else if (packet.code == COAP_DELETE){
        Serial.println("COAP_DELETE");
    } else {
        Serial.println("INVALID");
    }
    // Show message type
    Serial.print(" - Message Type:   ");
    if (packet.type == COAP_CON){
        Serial.println("COAP_CON");
    } else if (packet.type == COAP_NONCON){
        Serial.println("COAP_NONCON");
    } else {
        Serial.println("INVALID");
    }
    // Show payload Lenght
    Serial.print(" - Payload lenght: ");
    Serial.println(packet.payloadlen);
    // Show message ID
    Serial.print(" - Message ID:     ");
    Serial.println(packet.messageid);
    // End of log info
    Serial.println("\r==================================================\n\n\r");
}

void Coap_WellKnownCallback(CoapPacket &packet, IPAddress clientIp, int clientPort){
    // Log message info
    Coap_LogPacketInfo(packet);
    // evaluate method and perform action
    switch(packet.code){
        case COAP_GET:
            // Log the action and send response
            Serial.println("[Coap_WellKnownCallback] - Return the available resources");
            Coap.sendResponse(
                clientIp, 
                clientPort, 
                packet.messageid,
                "</.well-known/core>;d=Info of available resources,"
                "</light>n=Light;ct=51;d=Allowed methods GET & PUT,"
                "</button>n=Button;ct=51;d=Allowed methods GET"
            );
        break;
        // Return the same response for methods COAP_POST & COAP_DELETE (not allowed)
        case COAP_POST:
        case COAP_DELETE:
        case COAP_PUT:
            // Log the action and send Not Allowed response
            Serial.println("[Coap_WellKnownCallback] - Client has requested not allowed method");
            Coap.sendResponse(clientIp, clientPort, packet.messageid, NULL, 0, 
                COAP_METHOD_NOT_ALLOWD, COAP_NONE, packet.token, packet.tokenlen);
        break;
    }
}

void Coap_LightResourceCallback(CoapPacket &packet, IPAddress clientIp, int clientPort) {
    // Log message info
    Coap_LogPacketInfo(packet);
    // evaluate method and perform action
    switch(packet.code){
        case COAP_GET:
            // Log the action and send response
            Serial.println("[Coap_LightResourceCallback] - Return the LED status");
            Coap.sendResponse(
                clientIp, 
                clientPort, 
                packet.messageid,
                digitalRead(LED_ONBOARD) ? LIGHT_ON_RESPONSE_PAYLOAD : LIGHT_OFF_RESPONSE_PAYLOAD
            );
        break;
        // Return the same response for methods COAP_POST & COAP_DELETE (not allowed)
        case COAP_POST:
        case COAP_DELETE:
            // Log the action and send Not Allowed response
            Serial.println("[Coap_LightResourceCallback] - Client has requested not allowed method");
            Coap.sendResponse(clientIp, clientPort, packet.messageid, NULL, 0, 
                COAP_METHOD_NOT_ALLOWD, COAP_NONE, packet.token, packet.tokenlen);
        break;
        case COAP_PUT:
            // parse CoAP message payload (if received)
            char packetPayloadRaw[packet.payloadlen + 1];
            memcpy(packetPayloadRaw, packet.payload, packet.payloadlen);
            packetPayloadRaw[packet.payloadlen] = '\0';
            String message(packetPayloadRaw);
            // analyze request payload message
            if (message.equals(LIGHT_OFF_REQUEST_PAYLOAD)){
                // Write the new status in LED, send response and log action
                digitalWrite(LED_ONBOARD, false);
                Coap.sendResponse(clientIp, clientPort, packet.messageid, LIGHT_OFF_RESPONSE_PAYLOAD);
                Serial.println("[Coap_LightResourceCallback] Changing LED state to OFF");
            } else if(message.equals(LIGHT_ON_REQUEST_PAYLOAD)){
                digitalWrite(LED_ONBOARD, true);
                Coap.sendResponse(clientIp, clientPort, packet.messageid, LIGHT_ON_RESPONSE_PAYLOAD);
                Serial.println("[Coap_LightResourceCallback] Changing LED state to ON");
            } else {
                // Log the action and send Not Allowed response
                Serial.println("[Coap_LightResourceCallback] - Client has sent bad request");
                Coap.sendResponse(clientIp, clientPort, packet.messageid, NULL, 0, 
                    COAP_BAD_REQUEST, COAP_NONE, packet.token, packet.tokenlen);
            }
        break;
    }
}

void Coap_ButtonResourceCallback(CoapPacket &packet, IPAddress clientIp, int clientPort) {
    // Log message info
    Coap_LogPacketInfo(packet);
    // evaluate method and perform action
    switch(packet.code){
        case COAP_GET:
            // Log the action and send response
            Serial.println("[Coap_ButtonResourceCallback] - Return the Button status");
            Coap.sendResponse(
                clientIp, 
                clientPort, 
                packet.messageid,
                digitalRead(BUTTON_ONBOARD) ? BUTTON_NOT_PRESSED_RESPONSE_PAYLOAD : BUTTON_PRESSED_RESPONSE_PAYLOAD
            );
        break;
        // Return the same response for methods COAP_POST & COAP_DELETE (not allowed)
        case COAP_POST:
        case COAP_DELETE:
        case COAP_PUT:
            // Log the action and send Not Allowed response
            Serial.println("[Coap_ButtonResourceCallback] - Client has requested allowed method");
            Coap.sendResponse(clientIp, clientPort, packet.messageid, NULL, 0, 
                COAP_METHOD_NOT_ALLOWD, COAP_NONE, packet.token, packet.tokenlen);
        break;
    }
}

void Coap_ResponseCallback(CoapPacket &packet, IPAddress serverIp, int serverPort) {
    // parse CoAP message payload (if received)
    char payload[packet.payloadlen + 1];
    memcpy(payload, packet.payload, packet.payloadlen);
    payload[packet.payloadlen] = '\0';
    // Log the received payload
    Serial.print("[Coap_CallbackResponse] - Response received, payload: ");
    Serial.println(payload);
}

void App_Init(){
    // wait a moment before start
    delay(INIT_DELAY);
    // Configure serial port at 115200 baudrios
    Serial.begin(SERIAL_BAURDATE);
    // Configure pins of buttons and leds
    pinMode(LED_ONBOARD, OUTPUT);
    pinMode(BUTTON_ONBOARD, INPUT);
    // print to console Init message
    Serial.println("\n\n\rWelcome to CoAP Server Device - www.gotoiot.com");
    // connect to wifi network
    Wifi_EstablishConnection();
    // create the things that will be exposed
    Coap_InitServer();
    // put led in a known state
    digitalWrite(LED_ONBOARD, true);
}

void App_Loop(){
    Coap.loop();
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