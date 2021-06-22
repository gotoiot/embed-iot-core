# iBeacon Broadcaster

Aplicación para placa basada en ESP32 utilizando el framework Arduino y compilada con PlatformIO.

## Detalles de la aplicación 🔍

Este proyecto es una demostración completa de un broadcaster de tramas iBeacons utilizando una placa basada en el módulo ESP32. El dispositivo hace broadcasting de la trama iBeacon durante `IBEACON_ADVERTISING_DELAY` milisegundos y luego entra en modo deep sleep por `DEEP_SLEEP_SECONDS`. El valor que se transmite en cada trama iBeacon está determinado por las configuraciones `IBEACON_###` leídas desde el archivo `src/secrets.h`.

Para probar el código, copia el contenido del archivo `ibeacon_broadcaster.cpp` y pegalo dentro del archivo `src/main.cpp`. Luego configura el archivo `src/secrets.h` cargando con los valores adecuados los siguientes datos:

```cpp
// The general device ID
#define DEVICE_ID "generic-device-001"

// BLE settings
#define IBEACON_UUID            "ffeeddcc-bbaa-9988-7766-554433221100"
#define IBEACON_MANUFACTURER_ID 0x4C00
#define IBEACON_DEFAULT_MAJOR   11
#define IBEACON_DEFAULT_MINOR   22
```

La aplicación viene con una funcionalidad para cambiar el valor major y minor de la trama iBeacon si al iniciar, luego de un ciclo de deep sleep, se presiona el `BUTTON_ONBOARD`. Para el caso de las placas basadas en el ESP32 como NodeMCU o AlkESP32 el botón viene configurado en el pin 0 del microcontrolador. En caso que lo quieras cambiar o conectar un botón externo, deberías cambiar el valor `BUTTON_ONBOARD` de la aplicación. Así mismo viene con un contador de ciclos que indica la cantidad de paquetes enviados desde el último reinicio.

Debido a que el dispositivo entra en modo deep sleep - y todos los datos cargados en RAM se borran entre cada ejecución -, para poder persistir datos entre ciclos es necesario que se guarden con el tipo `RTC_DATA_ATTR`, como por ejemplo `RTC_DATA_ATTR static uint32_t BootCount;`.

Cuando tengas los datos cargados, abri una terminal con PlatformIO (como se indica en el README principal del proyecto) y ejecuta el comando `pio run -e default -t upload && pio device monitor` para cargar el programa en la placa y visualizarlo en la terminal serie. Deberias ver una salida como la siguiente:

```
Welcome to BLE iBeacon Broadcaster - www.gotoiot.com

iBeacon device has sent packages for 17 times
iBeacon data: {"uuid": ffeeddcc-bbaa-9988-7766-554433221100, "major": 11, "minor": 22, "tx_power": 0}
Stopping to advertise iBeacon package
Entering in deep sleep mode for 10 seconds
```

> Además de la información de la aplicación, en el monitor serie aparecen datos sobre el bootloader cuando comienza la ejecución desde deep sleep mode.

Una vez que el dispositivo se inicializa, realizará el envío de tramas iBeacon bajo el nombre de dispositivo `DEVICE_ID`, con el valor `IBEACON_UUID` y los valores major y minor seteados por defecto, o bien si se cambiaron mediante la pulsación del `ONBOARD_BUTTON`.

Para poder probar la funcionalidad completa del ejemplo, es necesario que tengas corriendo un iBeacon Observer dentro del rango de alcance del ESP32 y un cliente web adicional para visualizar los datos. Si no sabes como hacerlo, podes ver nuestro proyecto [Connection BLE](https://github.com/gotoiot/connection-ble), que se compone de un observer de beacons para escanear tramas y un cliente web para visualizar los valores del scanner en un navegador, formando así un ecosistema BLE completo.

## Autores 👥

Los autores de esta aplicación son: 

* **[Agustin Bassi](https://github.com/agustinBassi)**


## Licencia 📄

Este proyecto está bajo Licencia ([MIT](https://choosealicense.com/licenses/mit/)). Podés ver el archivo [LICENSE.md](LICENSE.md) para más detalles sobre el uso de este material.

---

**Copyright © Goto IoT 2021** - [**Website**](https://www.gotoiot.com) - [**Group**](https://groups.google.com/g/gotoiot) - [**Github**](https://www.github.com/gotoiot) - [**Twitter**](https://www.twitter.com/gotoiot) - [**Wiki**](https://github.com/gotoiot/doc/wiki)
