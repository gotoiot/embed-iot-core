# Embedded MQTT Client

**Autor**: Agustin Bassi - 2021

## Tabla de contenido

* [Información contextual](#Información-contextual)
* [Introducción](#introducción)
* [Instalar dependencias](#instalar-dependencias)
* [Descargar el código](#descargar-el-código)
* [Ejecutar la aplicación](#ejecutar-la-aplicación)
* [Colaborar](#colaborar)
* [Licencia](#licencia)

## Información contextual

> Para leer artículos relacionados con tecnologías IoT visitar nuestro sitio web [gotoiot.com](https://www.gotoiot.com).

> Para ver toda la documentación de los proyectos de manera abarcativa y organizada visitar nuestra [wiki de Goto IoT](https://github.com/gotoiot/doc/wiki).

> En caso de encontrar algún problema, comentarlo en nuestro [foro de Goto IoT](https://groups.google.com/g/gotoiot) para encontrar una solución entre los miembros de la comunidad.

> Muchos de los proyectos implementados en Goto IoT utilizan Visual Studio Code como IDE de desarrollo debido a su potencia y capacidad de instalar extensiones útiles de desarrollo, por lo que se recomienda descargarlo desde [este link](https://code.visualstudio.com/download). 

> Para poder probar el código es necesario contar con un broker MQTT. Consultar nuestra [sección de proyectos](https://www.gotoiot.com/pages/projects/) para encontrar información al respecto.

## Introducción

Este proyecto funciona como cliente MQTT embebido para conectarse a cualquier broker MQTT, ya sea de manera local o remota. El código publica topics que simulan mediciones de un sensor de presión y también se suscribe a un topic para cambiar la frecuencia con que se publican estas mediciones. De esta manera se tiene una demostración de comunicación bidireccional con un broker.

Está basado en el `framework Arduino`, y se compila y ejecuta con la herramienta [PlatformIO](https://platformio.org/install). El código original funciona para cualquier placa que contenga el `ESP32`, pero tambien es compatible con `ESP8266` y otras placas que soporten Arduino con conexión WiFi y MQTT. La configuración de la placa se encuentra en el archivo `platformio.ini`.

## Instalar dependencias

La herramienta utilizada para realizar la compilación y descarga del código es `PlatformIO`. Se recomienda instalarla dentro de Visual Studio Code, ya que mediante la extensión de PlatformIO se combina el poder un IDE multilenguaje como VS Code con las capacidades de administrar fácilmente los procesos de desarrollo de sistemas embebidos.

Realizar la instalación y configuración de PlatformIO dentro de VS Code siguiendo [nuestra guía paso a paso](https://www.gotoiot.com/pages/articles/platformio_vscode_installation/). 

Si es posible compilar un programa de ejemplo, continuar con el siguiente paso para descargar el código y ejecutarlo.

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