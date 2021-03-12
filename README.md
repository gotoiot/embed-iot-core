# Embedded IoT Plaform

**Autor**: Agustin Bassi - 2021

## Tabla de contenido

* [Introducción](#introducción)
* [Organización del proyecto](#organización-del-proyecto)
* [Instalar dependencias](#instalar-dependencias)
* [Descargar el código](#descargar-el-código)
* [Correr el programa por defecto](#correr-el-programa-por-defecto)
* [Ejecutar las aplicaciones](#ejecutar-las-aplicaciones)
* [Colaborar](#colaborar)
* [Licencia](#licencia)

## Introducción

Este proyecto es una plataforma integral para el desarrollo de aplicaciones embebidas enfocadas en IoT. Utiliza `Arduino` como framework de desarrollo y `PlatformIO` como toolchain de compilación, manejo de bibliotecas, y más. 

Viene cargado con ejemplos para distintos protocolos de IoT que se pueden compilar y ejecutar fácilmente. De esta manera se pueden probar diferentes tecnologías y comunicaciones desde un mismo repositorio, con un mismo esquema de trabajo y entendiendo una única documentación.

Entre los principales objetivos del proyecto se encuentran facilitar el desarrollo, centralizar el código, nuclear la información y probar aplicaciones lo más rapido posible.

Si bien se puede adaptar a distintas placas, está principalmente adaptado para correr con cualquiera que posea el módulo `ESP32`.

## Organización del proyecto

La organización del proyecto es simple y tiene este aspecto:

```sh
├── doc             # doc general del proyecto, imagenes, manuales, etc.
├── examples        # ejemplos de aplicaciones separadas por afinidad (mqtt, coap, ble, etc.)
├── lib             # bibliotecas externas gestionadas con PlaformIO
├── src             # donde se aloja el codigo fuente a compilar
|   ├── main.cpp    # archivo principal que contiene el codigo de la aplicacion
|   └── secrets.h   # archivo para guardar datos sensibles (contraseñas, hosts, etc.)
├── platformio.ini  # archivo de configuracion de compilacion (board, framework, libs, etc.)
├── README.md       # este archivo
└── LICENCE         # licencia del proyecto
```

## Instalar dependencias

Para correr proyecto es necesario instalar `PlatformIO` dentro del IDE `Visual Studio Code`. Este es uno de los IDEs de desarrollo más populares, y podes instalarlo desde su documentacion oficial en [este link](https://code.visualstudio.com/download). Para instalar PlatformIO en VS Code, en nuestra [guía de instalación paso a paso](https://www.gotoiot.com/pages/articles/platformio_vscode_installation/) estan todos los detalles para configurarlo y correr un programa de ejemplo.

Una vez que puedas correr el ejemplo de la guía, podes continuar con la descarga del código.

## Descargar el código

Para descargar el codigo, lo más conveniente es realizar un `fork` de este proyecto a tu cuenta personal haciendo click en [este link](https://github.com/gotoiot/embedded-iot-platform/fork). Una vez que ya tengas el fork a tu cuenta, descargalo con este comando (acordate de poner tu usuario en el link):

```
git clone https://github.com/TU_USUARIO/embedded-iot-platform.git
```

> En caso que no tengas una cuenta en Github podes clonar directamente este repo.

Abrí la carpeta del proyecto desde VS Code cuando descargues el código.

## Correr el programa por defecto

Para chequear que todo funcione correctamente vamos a compilar y ejecutar el programa por defecto. Vas a necesitar conectar la placa a la PC de desarrollo para poder programarla.

Lo primero es ir a la extensión de PlatformIO dentro de VS Code, y en la sección `Quick Access` seleccioná `Miscellaneous->New Terminal`. Esto carga la herramienta dentro del scope de la terminal. 

Luego, desde la raíz del proyecto corre este comando, que compila el código, lo descarga a la placa y abre una terminal serie; todo en un mismo comando:

```
pio run -t upload && pio device monitor
```

Cuando el programa inicie, el LED de la placa debería comenzar a blinkear y en la terminal serie debería verse una salida como esta:

```
Welcome Embedded IoT Platform - www.gotoiot.com
Device running
...
Device running
```

Si llegaste a este punto es porque todo está funcionando correctamente. De ahora en más podés centrarte en aprender cómo se corren las aplicaciones. Esto te va a permitir correr las que existen en el proyecto e incluso crear las tuyas de manera fácil y rápida.

## Ejecutar las aplicaciones

La ejecución de aplicaciones dentro del proyecto es muy sencilla. Selecciona de la carpeta `examples` el código que quieras correr. Los detalles de implementación de cada ejemplo están en el `README.md` de cada proyecto. Copia el contenido del archivo `example_name.cpp` del ejemplo, en el archivo `src/main.cpp`.

Después carga los datos sensibles que sean necesarios para la aplicación dentro del archivo `src/secrets.h`. En ese archivo se almacenan datos como por ejemplo el ID del dispositivo, las contraseñas de WiFi, las URL de hosts, credenciales, etc.

Una vez que tengas los secrets y el código cargado, con el comando `pio run -t upload && pio device monitor` vas a poder compilar, cargar el código y abrir la terminal serie. 

El comportamiento de cada aplicación está detallado en el `README` de cada proyecto, no olvides de chequearlo para ver cómo debería comportarse el dispositivo.


### Lista de aplicaciones

Las aplicaciones están ordenadas por afinidad y las que existen hasta el momento son las siguientes:

* **MQTT**
    * **Pressure measurer:** Es una demostración completa de comunicación bidireccional MQTT. Tiene la capacidad de enviar y recibir topics MQTT. Su funcionalidad principal radica en tomar mediciones "fake" de un sensor de presión y enviarlas en un topic determinado. El tiempo en que envía tales mediciones puede ser modificado enviando un topic de configuración desde otro cliente MQTT.

## Colaborar

¿Te gustó el proyecto? Si es así no dudes en apoyarlo con una estrella en Github desde [la home del proyecto](https://github.com/gotoiot/embedded-iot-platform), esto motiva mucho a seguir adelante con el desarrollo de código para la comunidad. Si estás interesado en recibir novedades cuando se hagan actualizaciones, podes suscribirte desde [este link](https://github.com/gotoiot/embedded-iot-platform/subscription).

Si te gustaría aplicar mejoras a este proyecto podes abrir un hilo de discusión en [este link](https://github.com/gotoiot/embedded-iot-platform/issues/new) para conversarlas y luego podrías enviarlas mediante un `pull request`. 

Finalmente podés compartir este proyecto para que más personas puedan utilizarlo y beneficiarse de esta gran comunidad del software libre.

## Licencia

[MIT](https://choosealicense.com/licenses/mit/)

![footer](doc/gotoiot-footer.png)