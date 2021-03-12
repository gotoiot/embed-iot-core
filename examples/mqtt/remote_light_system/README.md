# Remote light system

**Autor**: Agustin Bassi - 2021

## Detalles del proyecto

Este proyecto es una demostración abarcativa de las capacidades que tiene un dispositivo embebido para comunicarse por MQTT. Es capaz de enviar y recibir topics, enviar un topic al iniciar para dar aviso al sistema, así como también avisar automáticamente si sufre una desconexión (mensaje conocido como LWT). 

Su funcionalidad principal es actuar como un dispositivo de iluminación dentro de un sistema integral de luces que se controla de manera remota. Puede recibir un topic para controlar individualmente el LED de cada dispositivo asi como también se pueden controlar un grupo de dispositivos al mismo tiempo haciendo uso de la capacidad de broadcast de MQTT. También es capaz de informar el estado del dispositivo general, y el estado del LED. Esto puede permitir a sistemas remotos administrar y tener un control sobre el estado de cada dispositivo dentro de la red.

Para probar el código copia el contenido del archivo `remote_light_system.cpp` y pegalo dentro del archivo `src/main.cpp`. Luego configura el archivo `src/secrets.h` cargando con los valores adecuados los siguientes datos:

```cpp
// ID del dispositivo
#define DEVICE_ID            "YOUR_ID"
// Acceso a WiFi
const char WIFI_SSID[]     = "YOUR_WIFI_SSID";
const char WIFI_PASS[]     = "YOUR_WIFI_PASS";
// Conexion al host MQTT
const char     MQTT_HOST[] = "YOUR_MQTT_HOST"; // i.e: 192.168.0.106
const uint16_t MQTT_PORT   = 1883;
const char     MQTT_USER[] = "YOUR_USER";
const char     MQTT_PASS[] = "YOUR_PASS";
```

En caso que te conectes a un broker con usuario y contraseña sera necesario que configures `MQTT_USER` y `MQTT_PASS`. El resto de los secrets dejalos tal cual están.

Cuando tengas los datos cargados, abri una terminal con PlatformIO (como se indica en el README del proyecto) y ejecuta el comando `pio run -t upload && pio device monitor` para cargar el programa en la placa y visualizarlo en la terminal serie. Deberias ver una salida como la siguiente:

```
Welcome to Remote light system - www.gotoiot.com

Trying connection to Wifi SSID 'WiFi Secret'.
Wifi connected. Assigned device IP: '192.168.0.103'
Trying connection to MQTT broker '192.168.0.106:1883'
Connected to MQTT broker successfully
Subscribed to topic: /led/DEVICE_ID
Subscribed to topic: /status/DEVICE_ID
Subscribed to topic: /led/status/DEVICE_ID
Subscribed to topic: /all/led
Subscribed to topic: /all/led/status
Sending MQTT Topic '/up' -> '{"device_id":"DEVICE_ID","ip":"192.168.0.103","status":"running"}'
```

Una vez que el dispositivo inicializa envía al broker el topic `up` con un payload como este `'{"device_id":"DEVICE_ID","ip":"192.168.0.103","status":"running"}'`. Una vez enviado tal topic esta disponible para ser controlado o encuestado remotamente bajo las siguientes condiciones:

* Si recibe el topic `/led/DEVICE_ID` o bien el topic `/all/led` con un payload `on` u `off` encenderá/apagará el LED respectivamente.
* Si recibe el topic `/status/DEVICE_ID` envía un nuevo topic `/DEVICE_ID/status` con un payload similar a este `'{"device_id":"DEVICE_ID","ip":"192.168.0.103","status":"running"}'`.
* Si recibe el topic `/led/status/DEVICE_ID` o bien el topic `/all/led/status` envía un nuevo topic `/DEVICE_ID/led/status` con un payload similar a este `{"status":"off","time":85003}`.

En caso de desconectarse de manera inesperada envía el topic el topic `down` con un payload como este `'{"device_id":"DEVICE_ID"'`. Esto puede permitir a un sistema de control externo tener un control preciso del estado de funcionamiento de los dispositivos.

Para poder probar la funcionalidad completa del ejemplo, es necesario que tengas corriendo un broker MQTT y un cliente adicional. Si no sabes como hacerlo, podes ver nuestra aplicación [App MQTT Connection](https://github.com/gotoiot/app-mqtt-connection) que se compone de un broker MQTT, un cliente web para visualizar topics y este proyecto (o cualquier otro dentro de MQTT) para la parte embebida, armando así un ecosistema de comunicación completo.

## Licencia

[MIT](https://choosealicense.com/licenses/mit/)

![footer](../../../doc/gotoiot-footer.png)