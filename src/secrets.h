#ifndef __SECRETS_H__
#define __SECRETS_H__

#include <pgmspace.h>

// The general device ID
#define DEVICE_ID "generic-device-001"

// Wifi settings
const char WIFI_SSID[] = "";
const char WIFI_PASS[] = "";

// BLE settings
#define IBEACON_UUID            "ffeeddcc-bbaa-9988-7766-554433221100"
#define IBEACON_MANUFACTURER_ID 0x4C00
#define IBEACON_DEFAULT_MAJOR   11
#define IBEACON_DEFAULT_MINOR   22

// MQTT settings
const char     MQTT_HOST[] = "";
const uint16_t MQTT_PORT   = 0;
const char     MQTT_USER[] = "";
const char     MQTT_PASS[] = "";

// SSL Remote host Root CA 1
static const char SSL_CERT_CA[] PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
)EOF";

// SSL Device Certificate
static const char SSL_CERT_CRT[] PROGMEM = R"KEY(
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
)KEY";

// SSL Device Private Key
static const char SSL_CERT_PRIVATE[] PROGMEM = R"KEY(
-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----
)KEY";

#endif //__SECRETS_H__
