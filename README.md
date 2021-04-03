<p align="center">
    <a href="https://www.gotoiot.com/">
        <img src="doc/gotoiot-logo.png" alt="Logo" width="60" height="60">
    </a>
    <h2 align="center">Embed IoT Core</h2>
    <p align="center">
        Una plataforma embebida para desarrollo de proyectos IoT basada en Arduino y PlatformIO
        <br>
        <i>por Agustin Bassi - 2021</i>
    </p>
    <p align="center">
        <a href="https://github.com/gotoiot/embed-iot-core/graphs/contributors">
            <img src="https://img.shields.io/github/contributors/gotoiot/embed-iot-core.svg?style=for-the-badge" alt="Contributors">
        </a>
        <a href="https://github.com/gotoiot/embed-iot-core/network/members">
            <img src="https://img.shields.io/github/forks/gotoiot/embed-iot-core.svg?style=for-the-badge" alt="Forks">
        </a>
        <a href="https://github.com/gotoiot/embed-iot-core/stargazers">
            <img src="https://img.shields.io/github/stars/gotoiot/embed-iot-core.svg?style=for-the-badge" alt="Stargazers">
        </a>
        <a href="https://github.com/gotoiot/embed-iot-core/issues">
            <img src="https://img.shields.io/github/issues/gotoiot/embed-iot-core.svg?style=for-the-badge" alt="Issues">
        </a>
        <a href="https://github.com/gotoiot/embed-iot-core/blob/master/LICENSE.txt">
            <img src="https://img.shields.io/github/license/gotoiot/embed-iot-core.svg?style=for-the-badge" alt="Licence">
        </a>
    </p>
</p>

:star: Nos ayudarías mucho apoyando a este proyecto con una estrella en Github!

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

Entre los principales objetivos del proyecto se encuentran facilitar el desarrollo de aplicaciones embebidas IoT, centralizar el código, nuclear la información y probar aplicaciones lo más rapido posible.

Si bien se puede adaptar a distintas placas, está principalmente desarrollado para correr con cualquiera que posea el módulo `ESP32`.

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

Para correr proyecto es necesario instalar `PlatformIO` dentro del IDE `Visual Studio Code`. 

<details><summary><b>Mira las instrucciones de instalación</b></summary>
<br>

Este es uno de los IDEs de desarrollo más populares, y podes instalarlo desde su documentacion oficial en [este link](https://code.visualstudio.com/download). Para instalar PlatformIO en VS Code, en nuestra [guía de instalación paso a paso](https://www.gotoiot.com/pages/articles/platformio_vscode_installation/) estan todos los detalles para configurarlo y correr un programa de ejemplo.

Una vez que puedas correr el ejemplo de la guía, podes continuar con la descarga del código.

</details>

## Descargar el código

Para descargar el codigo, lo más conveniente es que realices un `fork` de este proyecto a tu cuenta personal haciendo click en [este link](https://github.com/gotoiot/embedded-iot-core/fork). Una vez que ya tengas el fork a tu cuenta, descargalo con este comando (acordate de poner tu usuario en el link):

```
git clone https://github.com/USER/embedded-iot-core.git
```

> En caso que no tengas una cuenta en Github podes clonar directamente este repo.

Abrí la carpeta del proyecto desde VS Code cuando descargues el código.

## Correr el programa por defecto

Para chequear que todo funcione correctamente lo conveniente es compilar y ejecutar el programa por defecto. 

<details><summary><b>Mira las instrucciones para correrlo</b></summary>
<br>

Como primera medida necesitas conectar la placa a la PC para poder programarla. Luego tenes que ir a la extensión de PlatformIO dentro de VS Code, y en la sección `Quick Access` seleccioná `Miscellaneous->New Terminal`. Esto carga la herramienta dentro del scope de la terminal. 

Luego, desde la raíz del proyecto corre este comando, que compila el código, lo descarga a la placa y abre una terminal serie; todo en un mismo comando:

```
pio run -t upload && pio device monitor
```

Cuando el programa inicie, el LED de la placa debería comenzar a blinkear y en la terminal serie debería verse una salida como esta:

```
Welcome Embedded IoT Core - www.gotoiot.com
Device running
...
Device running
```

Si llegaste a este punto es porque todo está funcionando correctamente. De ahora en más podés centrarte en aprender cómo se corren las aplicaciones. Esto te va a permitir correr las que existen en el proyecto e incluso crear las tuyas de manera fácil y rápida.

</details>

## Ejecutar las aplicaciones

La ejecución de aplicaciones dentro del proyecto es muy sencilla. 

<details><summary><b>Mira cómo correrlas</b></summary>
<br>

Selecciona de la carpeta `examples` el código que quieras correr. Los detalles de implementación de cada ejemplo están en el `README.md` de cada uno. Copia el contenido del archivo `.cpp` del ejemplo, en el archivo `src/main.cpp`.

Después carga los datos sensibles que sean necesarios para la aplicación dentro del archivo `src/secrets.h`. En ese archivo se almacenan datos como por ejemplo el ID del dispositivo, las contraseñas de WiFi, las URLs de hosts, credenciales, etc.

Una vez que tengas los secrets y el código cargado, con el comando `pio run -t upload && pio device monitor` vas a poder compilar, cargar el código y abrir la terminal serie. 

El comportamiento de cada aplicación está detallado en el README de cada proyecto, no olvides de chequearlo para ver cómo debería comportarse el dispositivo.

</details>

### Lista de aplicaciones

Las aplicaciones están ordenadas por afinidad y todas las que existen hasta el momento se listan aca.

<details><summary><b>Mira la lista completa</b></summary>
<br>

* **`MQTT`**
    * **[`Pressure measurer`](https://github.com/gotoiot/embed-iot-core/tree/master/examples/mqtt/pressure_measurer)**: Es una demostración completa de comunicación bidireccional MQTT. Tiene la capacidad de enviar y recibir topics MQTT. Su funcionalidad principal radica en tomar mediciones "fake" de un sensor de presión y enviarlas en un topic determinado. El tiempo en que envía tales mediciones puede ser modificado enviando un topic de configuración desde otro cliente MQTT. Accede al [README del proyecto](https://github.com/gotoiot/embed-iot-core/tree/master/examples/mqtt/pressure_measurer) para ver todos los detalles.<br><br>
    * **[`Remote light system`](https://github.com/gotoiot/embed-iot-core/tree/master/examples/mqtt/remote_light_system)**: es una demostración abarcativa de las capacidades que tiene un dispositivo embebido para comunicarse por MQTT. Es capaz de enviar y recibir topics, enviar un topic al iniciar para dar aviso al sistema, así como también avisar automáticamente si sufre una desconexión (mensaje conocido como LWT). Su funcionalidad principal es actuar como un dispositivo de iluminación dentro de un sistema integral de luces que se controla de manera remota. Puede recibir un topic para controlar individualmente el LED de cada dispositivo asi como también se pueden controlar un grupo de dispositivos al mismo tiempo haciendo uso de la capacidad de broadcast de MQTT. También es capaz de informar el estado del dispositivo general, y el estado del LED. Esto puede permitir a sistemas remotos administrar y tener un control sobre el estado de cada dispositivo dentro de la red. Accede al [README del proyecto](https://github.com/gotoiot/embed-iot-core/tree/master/examples/mqtt/remote_light_system) para ver todos los detalles.

</details>

## Colaborar

¿Te gustó el proyecto? Si es así no dudes en apoyarlo con una :star: en Github desde [la home del proyecto](https://github.com/gotoiot/embed-iot-core), esto motiva mucho a seguir adelante con el desarrollo de código para la comunidad. Si estás interesado en recibir novedades cuando se hagan actualizaciones, podes suscribirte desde [este link](https://github.com/gotoiot/embed-iot-core/subscription).

Si te gustaría aplicar mejoras a este proyecto podes abrir un hilo de discusión en [este link](https://github.com/gotoiot/embed-iot-core/issues/new) para conversarlas y luego podrías enviarlas mediante un `pull request`. 

Finalmente podés compartir este proyecto para que más personas puedan utilizarlo y beneficiarse de esta gran comunidad del software libre.

## Licencia

[MIT](https://choosealicense.com/licenses/mit/)

## Acerca de Goto IoT

Estos son los links más relevantes para que puedas mantenerte al tanto de novedades y actualizaciones:

* **[Sitio web](https://www.gotoiot.com/):** Donde se publican los artículos y proyectos sobre IoT. 
* **[Github de Goto IoT:](https://github.com/gotoiot)** Donde están todos los proyectos para descargar y utilizar. 
* **[Foro de Goto IoT:](https://groups.google.com/g/gotoiot)** Donde los miembros del grupo realizan consultas técnicas, solucionan problemas y comparten novedades.
* **[Twitter de Goto IoT:](https://twitter.com/gotoiot)** Donde se publican novedades como nuevos proyectos y artículos, así como también temas relacionados con la materia.

![footer](doc/gotoiot-footer.png)