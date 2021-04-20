<a href="https://www.gotoiot.com/">
    <img src="doc/gotoiot-logo.png" alt="logo" title="Goto IoT" align="right" width="60" height="60" />
</a>

Embed IoT Core
==============

*Ayudaría mucho si apoyaras este proyecto con una ⭐ en Github!*


Este proyecto es una plataforma integral para el desarrollo de aplicaciones embebidas enfocadas en IoT. Utiliza `Arduino` como framework de desarrollo y `PlatformIO` como toolchain de compilación, manejo de bibliotecas, y más. Viene cargado con varias aplicaciones de ejemplo para distintos protocolos de IoT que se pueden compilar y ejecutar fácilmente. 

Con esta plataforma se pueden probar diferentes tecnologías y comunicaciones desde un mismo repositorio, con un mismo esquema de trabajo y entendiendo una única documentación.

El objetivo de Embed IoT Core es facilitar el desarrollo de aplicaciones embebidas IoT, centralizar el código y la documentación, y probar aplicaciones lo más rapido posible.

Si bien se puede adaptar a distintas placas, está principalmente desarrollado para correr sobre el módulo `ESP32`.

## Comenzando 🚀

Esta sección es una guía con los pasos escenciales para que puedas poner en marcha la plataforma. Vas a necesitar una placa con el módulo `ESP32` u otra compatible con `Arduino`.

<details><summary><b>Mira los pasos necesarios</b></summary><br>

### Instalar las dependencias

Para correr proyecto es necesario instalar `PlatformIO` dentro del IDE `Visual Studio Code`. 

Este es uno de los IDEs de desarrollo más populares, y podés instalarlo desde su documentacion oficial en [este link](https://code.visualstudio.com/download). Para instalar PlatformIO en VS Code, en nuestra [guía de instalación paso a paso](https://www.gotoiot.com/pages/articles/platformio_vscode_installation/) estan todos los detalles para configurarlo y correr un programa de ejemplo.

Una vez que puedas correr el ejemplo de la guía, podes continuar con la descarga del código.

### Descargar el código

Para descargar el código, lo más conveniente es que realices un `fork` de este proyecto a tu cuenta personal haciendo click en [este link](https://github.com/gotoiot/embed-iot-core/fork). Una vez que ya tengas el fork a tu cuenta, descargalo con este comando (acordate de poner tu usuario en el link):

```
git clone https://github.com/USER/embed-iot-core.git
```

> En caso que no tengas una cuenta en Github podes clonar directamente este repo.

### Correr el programa por defecto

Para chequear que todo funcione correctamente lo conveniente es compilar y ejecutar el programa por defecto. 

Como primera medida necesitas conectar la placa a la PC para poder programarla. Luego tenes que ir a la extensión de PlatformIO dentro de VS Code, y en la sección `Quick Access` seleccioná `Miscellaneous->New Terminal`. Esto carga la herramienta dentro del scope de la terminal. 

Luego, desde la raíz del proyecto corre este comando, que compila el código, lo descarga a la placa y abre una terminal serie; todo en un mismo comando:

```
pio run -t upload && pio device monitor
```

Cuando el programa inicie, el LED de la placa debería comenzar a blinkear y en la terminal serie debería verse una salida como esta:

```
Welcome Embed IoT Core - www.gotoiot.com
Device running
...
Device running
```

Si llegaste a este punto es porque todo está funcionando correctamente.

</details>

Continuá explorando el proyecto una vez que lo tengas funcionando.

## Configuraciones de funcionamiento 🔩

Las configuraciones del proyecto se basan principalmente en cargar las aplicaciones existentes y cómo crear tus propias aplicaciones embebidas.

<details><summary><b>Lee cómo configurar la plataforma</b></summary>

### Ejecutar las aplicaciones

La ejecución de aplicaciones dentro del proyecto es muy sencilla. 

Selecciona de la carpeta `examples` el código que quieras correr. Los detalles de implementación de cada ejemplo están en el `README.md` de cada uno. Copia el contenido del archivo `.cpp` del ejemplo, en el archivo `src/main.cpp`.

Después carga los datos sensibles que sean necesarios para la aplicación dentro del archivo `src/secrets.h`. En ese archivo se almacenan datos como por ejemplo el ID del dispositivo, las contraseñas de WiFi, las URLs de hosts, credenciales, etc.

Una vez que tengas los secrets y el código cargado, con el comando `pio run -t upload && pio device monitor` vas a poder compilar, cargar el código y abrir la terminal serie. 

El comportamiento de cada aplicación está detallado en el README de cada proyecto, no olvides de chequearlo para ver cómo debería comportarse el dispositivo.

### Crear tus propias aplicaciones

En el caso que quieras crear tu aplicación deberías copiar dentro de la carpeta `examples` algún ejemplo que ya te sirva y comenzar a editar el código dentro del archivo `.cpp`. 

Una vez tengas la aplicación más definida podés comenzar un proceso de iteración en el archivo `src/main.cpp`, ir compilando y ejecutando código en la placa. Vas a necesitar configurar el archivo `secrets.h` adecuadamente en este punto.

Una vez que tengas los secrets y el código cargado, con el comando `pio run -t upload && pio device monitor` vas a poder compilar, cargar el código y abrir la terminal serie. 

</details>

## Detalles principales 🔍

En esta sección vas a encontrar las características más relevantes del proyecto.

<details><summary><b>Mira los detalles más importantes</b></summary><br>

### Organización del proyecto

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

### Lista de aplicaciones

Las aplicaciones están ordenadas por afinidad y todas las que existen hasta el momento se listan aca.

* **`MQTT`**
    * **[`Pressure measurer`](https://github.com/gotoiot/embed-iot-core/tree/master/examples/mqtt/pressure_measurer)**: Es una demostración completa de comunicación bidireccional MQTT. Tiene la capacidad de enviar y recibir topics MQTT. Su funcionalidad principal radica en tomar mediciones "fake" de un sensor de presión y enviarlas en un topic determinado. El tiempo en que envía tales mediciones puede ser modificado enviando un topic de configuración desde otro cliente MQTT. Accede al [README del proyecto](https://github.com/gotoiot/embed-iot-core/tree/master/examples/mqtt/pressure_measurer) para ver todos los detalles.<br><br>
    * **[`Remote light system`](https://github.com/gotoiot/embed-iot-core/tree/master/examples/mqtt/remote_light_system)**: es una demostración abarcativa de las capacidades que tiene un dispositivo embebido para comunicarse por MQTT. Es capaz de enviar y recibir topics, enviar un topic al iniciar para dar aviso al sistema, así como también avisar automáticamente si sufre una desconexión (mensaje conocido como LWT). Su funcionalidad principal es actuar como un dispositivo de iluminación dentro de un sistema integral de luces que se controla de manera remota. Puede recibir un topic para controlar individualmente el LED de cada dispositivo asi como también se pueden controlar un grupo de dispositivos al mismo tiempo haciendo uso de la capacidad de broadcast de MQTT. También es capaz de informar el estado del dispositivo general, y el estado del LED. Esto puede permitir a sistemas remotos administrar y tener un control sobre el estado de cada dispositivo dentro de la red. Accede al [README del proyecto](https://github.com/gotoiot/embed-iot-core/tree/master/examples/mqtt/remote_light_system) para ver todos los detalles.


</details>

## Tecnologías utilizadas 🛠️

Estas son las tecnologías más importantes utilizadas.

<details><summary><b>Mira la lista completa de tecnologías</b></summary><br>

* [PlatformIO](https://platformio.org/n) - Plataforma para desarrollar sistemas embebidos.
* [Visual Studio Code](https://code.visualstudio.com/) - Popular IDE de desarrollo para múltiples plataformas.
* [Arduino](http://arduino.cc/) - Framework para desarrollo de sistemas embebidos.
* [Espressif ESP32](https://www.espressif.com/en/products/socs/esp32) - SoC con WiFi y Bluetooth integrado ampliamente utilizado en IoT.

</details>

## Contribuir 🖇️

Si estás interesado en el proyecto y te gustaría sumar fuerzas para que siga creciendo y mejorando, podés abrir un hilo de discusión para charlar tus propuestas en [este link](https://github.com/gotoiot/embed-iot-core/issues/new). Así mismo podés leer el archivo [Contribuir.md](https://github.com/gotoiot/gotoiot-doc/wiki/Contribuir) de nuestra Wiki donde están bien explicados los pasos para que puedas enviarnos pull requests.


## Autores 👥

Las colaboraciones principales fueron realizadas por:

* **[Agustin Bassi](https://github.com/agustinBassi)**: Ideación, puesta en marcha y mantenimiento del proyecto.

También podés mirar todas las personas que han participado en la [lista completa de contribuyentes](https://github.com/embed-iot-core/contributors).


## Sobre Goto IoT 📖

Goto IoT es una plataforma que publica material y proyectos de código abierto bien documentados junto a una comunidad libre que colabora y promueve el conocimiento sobre IoT entre sus miembros. Acá podés ver los links más importantes:

* **[Sitio web](https://www.gotoiot.com/):** Donde se publican los artículos y proyectos sobre IoT. 
* **[Github de Goto IoT:](https://github.com/gotoiot)** Donde están alojados los proyectos para descargar y utilizar. 
* **[Comunidad de Goto IoT:](https://groups.google.com/g/gotoiot)** Donde los miembros de la comunidad intercambian información e ideas, realizan consultas, solucionan problemas y comparten novedades.
* **[Twitter de Goto IoT:](https://twitter.com/gotoiot)** Donde se publican las novedades del sitio y temas relacionados con IoT.
* **[Wiki de Goto IoT:](https://github.com/gotoiot/doc/wiki)** Donde hay información de desarrollo complementaria para ampliar el contexto.

## Muestas de agradecimiento 🎁

Si te gustó este proyecto y quisieras apoyarlo, cualquiera de estas acciones estaría más que bien para nosotros:

* Apoyar este proyecto con una ⭐ en Github para llegar a más personas.
* Sumarte a [nuestra comunidad](https://groups.google.com/g/gotoiot) abierta y dejar un feedback sobre qué te pareció el proyecto.
* [Seguirnos en twitter](https://github.com/gotoiot/doc/wiki) y dejar algún comentario o like.
* Compartir este proyecto con otras personas.

## Licencia 📄

Este proyecto está bajo Licencia ([MIT](https://choosealicense.com/licenses/mit/)). Podés ver el archivo [LICENSE.md](LICENSE.md) para más detalles sobre el uso de este material.

---

**Copyright © Goto IoT 2021** ⌨️ [**Website**](https://www.gotoiot.com) ⌨️ [**Group**](https://groups.google.com/g/gotoiot) ⌨️ [**Github**](https://www.github.com/gotoiot) ⌨️ [**Twitter**](https://www.twitter.com/gotoiot) ⌨️ [**Wiki**](https://github.com/gotoiot/doc/wiki)
