# Pressure Measurer

**Autor**: Agustin Bassi - 2021

## Detalles del proyecto

Este proyecto es una demostración completa de comunicación bidireccional MQTT. Tiene la capacidad de enviar y recibir topics. Su funcionalidad principal radica en tomar mediciones "fake" de un sensor de presión y enviarlas en un topic cada determinado tiempo. El tiempo en que envía tales mediciones puede ser modificado enviando un topic de configuración.

Para probar el código copia el contenido del archivo `pressure_measurer.cpp` y pegalo dentro del archivo `src/main.cpp`. Luego configura el archivo `src/secrets.h` cargando con los valores adecuados los siguientes datos:

```cpp
// ID del dispositivo
#define DEVICE_ID            "YOUR_ID"
// Acceso a WiFi
const char WIFI_SSID[]     = "YOUR_WIFI_SSID";
const char WIFI_PASS[]     = "YOUR_WIFI_PASS";
// Conexion al host MQTT
const char     MQTT_HOST[] = "YOUR_MQTT_HOST"; // i.e: 192.168.0.106
const uint16_t MQTT_PORT   = 1883;
const char     MQTT_USER[] = "";
const char     MQTT_PASS[] = "";
```

En caso que te conectes a un broker con usuario y contraseña sera necesario que configures `MQTT_USER` y `MQTT_PASS`. El resto de los secrets dejalos tal cual están.

Cuando tengas los datos cargados, abri una terminal con PlatformIO (como se indica en el README del proyecto) y ejecuta el comando `pio run -t upload && pio device monitor` para cargar el programa en la placa y visualizarlo en la terminal serie. Deberias ver una salida como la siguiente:

```
Welcome to Pressure Measurer - www.gotoiot.com

Trying connection to Wifi SSID 'WIFI_SSID'.
Wifi connected. Assigned device IP: '192.168.0.103'
Subscribed to topic: 'DEVICE_ID/config'
Subscribed to topic: 'DEVICE_ID/status/get'
Sending MQTT Topic 'up' -> '{"device_id": "DEVICE_ID, "ip": "192.168.0.103", "status": "running"}'
Sending MQTT Topic 'DEVICE_ID/pressure'->'{"value": 55, "measure": "psi", "time": 12340074}
...
Sending MQTT Topic 'DEVICE_ID/pressure'->'{ "value": 83, "measure": "psi", "time": 448821023}
```

Una vez que el dispositivo se inicializa, comienza a enviar mediciones periódicas del sensor fake de presion en el topic `DEVICE_ID/pressure`. 

Así mismo se suscribe al topic `DEVICE_ID/config`, donde espera recibir el valor de publicación de las mediciones de presión en milisegundos (entre 1000 y 10000). En el caso de recibir un valor adecuado, en la terminal serie se mostrará un mensaje similar al siguiente: `Publish time will change to 2500 ms`.

También se suscribe al topic `DEVICE_ID/status/get`, que al momento de recibirlo, el dispositivo publica en el topic `DEVICE_ID/status` un mensaje similar al siguiente:

```json
{
    "value": 55,
    "unit": "psi",
    "time": 12340074
}
```

Para poder probar la funcionalidad completa del ejemplo, es necesario que tengas corriendo un broker MQTT y un cliente adicional. Si no sabes como hacerlo, podes ver nuestro proyecto [Connection MQTT](https://github.com/gotoiot/connection-mqtt), que se compone de un broker y distintos servicios relacionados que conforman un ecosistema MQTT completo.

## Licencia

[MIT](https://choosealicense.com/licenses/mit/)

![footer](../../../doc/gotoiot-footer.png)