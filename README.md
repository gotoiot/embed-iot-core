# Embedded MQTT Client

**Autor**: Agustin Bassi - 2021

## Tabla de contenido

* [Introducción](#introducción)
* [Instalar dependencias](#instalar-dependencias)
* [Descargar el código](#descargar-el-código)
* [Ejecutar la aplicación](#ejecutar-la-aplicación)
* [Colaborar](#colaborar)
* [Licencia](#licencia)

## Introducción

> Si todavía no conoces como está estructurada la plataforma Goto IoT es recomendable que leas la [información contextual](https://github.com/gotoiot/doc/wiki#informaci%C3%B3n-contextual) de nuestra wiki, que te puede ser de utilidad.

Este proyecto funciona como cliente MQTT embebido para conectarse a cualquier broker MQTT, ya sea de manera local o remota. El código publica topics que simulan mediciones de un sensor de presión y también se suscribe a un topic para cambiar la frecuencia con que se publican estas mediciones. De esta manera se tiene una demostración de comunicación bidireccional con un broker.

Está basado en el `framework Arduino`, y se compila y ejecuta con la herramienta `PlatformIO`. El código original funciona para cualquier placa que contenga el `ESP32`, pero tambien es compatible con `ESP8266` y otras placas que soporten Arduino con conexión WiFi y MQTT. La configuración de la placa se encuentra en el archivo `platformio.ini`.

## Instalar dependencias

Para correr proyecto es necesario tener instalado `PlaformIO` dentro de Visual Studio Code. En la sección de [instalación de herramientas](https://github.com/gotoiot/doc/wiki/Herramientas#instalaci%C3%B3n) de la wiki se encuentran los detalles para realizar la instalación y configuración.

Así mismo será necesario contar con un broker MQTT corriendo para realizar las pruebas. En la [sección de proyectos de la web](https://www.gotoiot.com/pages/projects) o bien dentro de los [repositorios de Goto IoT](https://github.com/gotoiot?q=mqtt) se puede encontrar información al respecto.

## Descargar el código

Desde la esquina superior derecha realizar un `fork` de este proyecto a la cuenta personal. Una vez realizado el fork descargar el código con el siguiente comando (poner el usuario de Github en la URL):

```
git clone https://github.com/USER/embedded-mqtt-client.git
```

> En caso de no poseer una cuenta de Github se puede realizar un `clone` directo de este repositorio.

Abrir la carpeta del proyecto desde VS Code luego de la descarga.

## Ejecutar la aplicación


Como primer paso será necesario configurar el acceso a WiFi y MQTT dentro del archivo `src/main.cpp` (líneas 48-52):

```c
// Wifi settings
const String WIFI_SSID   = "USER_WIFI_SSID";
const String WIFI_PASS   = "USER_WIFI_PASSWORD";
// Mqtt server settings
const String MQTT_SERVER = "MQTT_HOST_IP_ADDRESS";
const String MQTT_PORT   = 1883;
```

Conectar luego la placa por USB y dentro de VS Code ir a la extensión PlatformIO en el borde izquierdo, y dentro del menú lateral ir a `Quick Acess->Miscellaneous->New Terminal`. En la nueva terminal ejecutar el siguiente comando, que se encarga de compilar el código, descargarlo a la placa y abrir automáticamente el puerto serie, todo en una misma operación.

```sh
platformio run --target upload && platformio device monitor
```

Cuando el dispositivo inicia debería mostrarse una salida como la siguiente:

```sh
Welcome to Embedded MQTT Client - www.gotoiot.com
Connecting to WiFi SSID...
WiFi connected
IP address: 192.168.1.44
Attempting MQTT connection...connected
Subscribed to topic: mqtt-client-001/config/publish_time
Sending MQTT Topic-Payload: mqtt-client-001/pressure -> 1001
...
Sending MQTT Topic-Payload: mqtt-client-001/pressure -> 1010
```

Para probar que la recepción de topics funcione correctamente, através de otro cliente MQTT conectado al broker, enviar un mensaje al dispositivo con el topic `mqtt-client-001/config/publish_time` con un valor entre 1000 y 10000 (en ms). Esto cambiará el período con que el dispositivo publica los topics entre 1-10 segundos.

## Colaborar

Las mejoras son bienvenidas. Para ello es necesario hacer un fork de este proyecto, aplicar las mejoras y enviarlas mediante un pull request. Luego de la revisión, podrán ser incluídas.

Si te gustó el proyecto no dudes en apoyarlo con una `Star`, y si estás interesado en recibir novedades podés aplicar un `Watch`. Estas acciones ayudan a fomentar la participación y creación de nuevos proyectos dentro de [Goto IoT](https://github.com/gotoiot/).

## Licencia

[MIT](https://choosealicense.com/licenses/mit/)

![footer](doc/gotoiot-footer.png)