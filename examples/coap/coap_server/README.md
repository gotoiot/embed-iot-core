# CoAP Server

Aplicaci贸n para ESP32 o similar basada en Arduino y compilada con PlatformIO.

## Detalles de la aplicaci贸n 馃攳

Este proyecto es una demostraci贸n completa de un servidor CoAP que habilita diferentes recursos (endpoints) que un cliente CoAP puede encuestar. Como esta pensado para funcionar en un dispositivo como un ESP32 - que generalmente vienen integrados con un boton y un LED - esta aplicaci贸n crea un recurso asociado al LED onboard de la placa para poder controlarlo y otro asociado al bot贸n, de manera tal que se puede encuestar el estado del mismo. Adem谩s, implementa el recurso `well-known` que permite descubrir los recursos que implementa el servidor.

Para probar el c贸digo copia el contenido del archivo `coap_server.cpp` y pegalo dentro del archivo `src/main.cpp`. Luego configura el archivo `src/secrets.h` cargando con los valores adecuados los siguientes datos:

```cpp
// ID del dispositivo
#define DEVICE_ID            "YOUR_ID"
// Acceso a WiFi
const char WIFI_SSID[]     = "YOUR_WIFI_SSID";
const char WIFI_PASS[]     = "YOUR_WIFI_PASS";
```

Cuando tengas los datos cargados, abri una terminal con PlatformIO (como se indica en el README principal del proyecto) y ejecuta el comando `pio run -e default -t upload && pio device monitor` para cargar el programa en la placa y visualizarlo en la terminal serie. Deberias ver una salida como la siguiente:

```
Welcome to  CoAP Server Device - www.gotoiot.com

Trying connection to Wifi SSID 'WIFI_SSID'.
Wifi connected. Assigned device IP: '192.168.0.103'
[Coap_InitServer] - Setup Callback Light
[Coap_InitServer] - Setup Callback Button
[Coap_InitServer] - Setup Callback Well known
[Coap_InitServer] - Setup Response Callback
```

Una vez que el dispositivo se inicializa, intenta conectarse a WiFi tomando las configuraciones `WIFI_SSID` y `WIFI_PASS` que configuraste en el archivo `secrets.h`. Luego, inicializa los recursos CoAP correspondientes a `Light`, `Button` y `Well known` y se queda a la espera de requests provenientes de un cliente.

Como podr谩s observar en el c贸digo, cada recurso tiene sus propios m茅todos permitidos. El recurso Light admite los m茅todos GET y PUT, y los recursos Button y Well Known solo admiten el m茅todo GET. Para otros requests que ejecutes el server responder谩 con un mensaje de error adecuadamente.

As铆 mismo, para poder analizar los mensajes que se env铆an y reciben, el server imprime en la terminal serie las descripciones de los mismos. En la siguiente salida pod茅s ver un ejemplo:

```sh
==================================================
Coap_LogPacketInfo
------------------

 - Method:         COAP_GET
 - Message Type:   COAP_CON
 - Payload lenght: 0
 - Message ID:     2557
==================================================
```

## Testear el server

Para testear el server CoAP pod茅s usar cualquier cliente. Para este caso te proponemos usar un contenedor de Docker con la herramienta libcoap instalada. Para ello comenz谩 descargando el contenedor con el siguiente comando:

```sh
docker pull abassi/libcoap:latest
```

* Obtener el recurso `.well-known/core`, para que el server responda con los recursos disponibles.

```sh
docker run --rm --net=host -it abassi/libcoap \
coap-client -m get -p 5683 coap://IP_SERVER/.well-known/core
```

* Obtener el estado del recurso `light`.

```sh
docker run --rm --net=host -it abassi/libcoap \
coap-client -m get -p 5683 coap://IP_SERVER/light
```

* Actualizar el estado del recurso `light` poniendolo en ON.

```sh
docker run --rm --net=host -it abassi/libcoap \
coap-client -m put -e '{"light":true}' -p 5683 coap://IP_SERVER/light
```

* Actualizar el estado del recurso `light` poniendolo en OFF.

```sh
docker run --rm --net=host -it abassi/libcoap \
coap-client -m put -e '{"light":false}' -p 5683 coap://IP_SERVER/light
```

* Obtener el estado del recurso `button`.

```sh
docker run --rm --net=host -it abassi/libcoap \
coap-client -m get -p 5683 coap://IP_SERVER/button
```

* Testear la respuesta cuando el server no encuentra el recurso solicitado.

```sh
docker run --rm --net=host -it abassi/libcoap \
coap-client -m get -p 5683 coap://IP_SERVER/not/found/resource
```

* Testear la respuesta para un metodo no permitido dentro de un recurso. 

```sh
docker run --rm --net=host -it abassi/libcoap \
coap-client -m post -e '{"light":true}' -p 5683 coap://IP_SERVER/light
```

* Testear un request mal formado para un recurso dentro del server.

```sh
docker run --rm --net=host -it abassi/libcoap \
coap-client -m post -e '{"light":invalid_state}' -p 5683 coap://IP_SERVER/light
```


## Autores 馃懃

Los autores de esta aplicaci贸n son: 

* **[Agustin Bassi](https://github.com/agustinBassi)**


## Licencia 馃搫

Este proyecto est谩 bajo Licencia ([MIT](https://choosealicense.com/licenses/mit/)). Pod茅s ver el archivo [LICENSE.md](LICENSE.md) para m谩s detalles sobre el uso de este material.

---

**Copyright 漏 Goto IoT 2021** - [**Website**](https://www.gotoiot.com) - [**Group**](https://groups.google.com/g/gotoiot) - [**Github**](https://www.github.com/gotoiot) - [**Twitter**](https://www.twitter.com/gotoiot) - [**Wiki**](https://github.com/gotoiot/doc/wiki)