![header](doc/header.png)

# Open source MQTT Platform

Author: Agustin Bassi - 2020

## 
## Table of Contents


* [Platform Introduction](#platform-introduction)
* [Install dependencies](#install-dependencies)
* [Run the application](#run-the-application)
* [Test the application](#test-the-application)
* [Run mqtt-client-arduino (optional)](#run-mqtt-client-arduino-(optional))
* [Want to help?](#want-to-help-?)
* [License](#license)

## 
## Platform Description

The goal of this project is to create an open source MQTT Platform to be used as a part of an IoT system, based on MQTT protocol.

The platform consists in several modules described below (All of them are well described in the [Project Wiki](https://github.com/agustinBassi/mq-connection/wiki)).

* **MQTT Broker**: Raspberry Pi that runs a MQTT Broker to interact with the HTTP client via WebSockets and to MQTT clients via MQTT protocol. Besides, has a HTTP server in order to serve the page of the HTTP Client.
* **MQTT Client Web**: A Single Page Application (SPA) that communicates with MQTT Broker via Websockets. It can send and receive MQTT topics and perform many actions. The code used for MQTT connection is based on [this project](https://github.com/jpmens/simple-mqtt-websocket-example).
* **MQTT Client Arduino**: A device that connects to MQTT Broker in order to establish a connection to send/receive topics. The device connects to WiFi and then, connects to the MQTT Broker. 

In the figure below there is a description of the platform modules and how they interact each others.

![architecture](doc/architecture.png)

## 
## Install dependencies


The application runs over Raspberry Pi 3+. To install Raspberry Pi OS refer to [official documentation](https://www.raspberrypi.org/documentation/installation/installing-images/).

The platform needs the next dependencies.

* Docker & Docker-Compose (installation steps in [this link](https://devdojo.com/bobbyiliev/how-to-install-docker-and-docker-compose-on-raspberry-pi)).

_Although the application is designed to run on a Raspberry Pi 3+, it can runs on any system with Docker & Docker Compose installed. Docker installation steps in [official documentation](https://docs.docker.com/get-docker/). Docker-Compose installation steps in [official documentation](https://docs.docker.com/compose/install/)._

## 
## Run the application

Once dependencies are installed in the Raspberry Pi do the next steps.

1. Download the platform code (this repository) with the next command.

```
git clone https://github.com/agustinBassi/mq-connection.git
cd mq-connection/
```

2. Start the MQTT Broker and the HTTP server with the next command.

```
docker-compose up
```

3. Run the MQTT Web Client opening [http://raspberri_pi_ip:5001/](http://raspberri_pi_ip:5001/) in the web browser.

## 
## Test the application

To test broker-client communication open `mqtt-client-web` in the browser (step 3 above). 

1. Set the MQTT host IP in the field `MQTT host`, set an appropiate `Port` (default 9001) and `MQTT Client` and press the button `CONNECT` to connect to broker. 
2. Set a `Topic to subscribe` and press the button `SUBSCRIBE` to receive messages from broker (default all topic '#').
3. Set a `Topic to publish` and `Payload to publish` and press `PUBLISH` to send a message to broker.

In the next figure there is an example of connection to MQTT host at 192.168.0.202 IP address, at 9001 port setting client as test-client-001. In the log lines can be seen steps done (1,2,3).

![mqtt-client-web-running](doc/mqtt-web-client-running.png)

Try to subscribe or publish messages from another clients in order to see how interacts web client with the others through the MQTT broker.

## 
## Run mqtt-client-arduino (optional)

To run the `mqtt-client-arduino` it is necessary to have installed [PlatformIO](https://platformio.org/) in order to compile the project and upload the code into the board. In [this link](https://iot-es.herokuapp.com/post/details/17) there is a guide to install PlatformIO for Visual Studio Code, compile and run a project. More details in the [Project Wiki](https://github.com/agustinBassi/mq-connection/wiki).

Once PlatformIO is installed, set WiFi access and MQTT host IP address properly (the IP of the Raspberry Pi) in the file `mqtt-client-arduino/src/main.cpp` as follow (lines 48-52).

```c
// Wifi settings
const String WIFI_SSID   = "USER_WIFI_SSID";
const String WIFI_PASS   = "USER_WIFI_PASSWORD";
// Mqtt server settings
const String MQTT_SERVER = "MQTT_HOST_IP_ADDRESS";
```

Then, plug the embedded device via USB and run the command below to compile, upload the code into the board and open the serial monitor, all in the same operation (Change `platformio` for `pio` if command fails).

```sh
platformio run --target upload && platformio device monitor
```

When device starts to run, an output link below should be shown.

```sh
Welcome to MQ Connection Arduino client!
Connecting to WiFi SSID...
WiFi connected
IP address: 192.168.1.44
Attempting MQTT connection...connected
Subscribed to topic: MQ-connection-esp32-1/config/publish_time
Sending MQTT Topic-Payload: MQ-connection-esp32-1/pressure -> 1001
...
Sending MQTT Topic-Payload: MQ-connection-esp32-1/pressure -> 1010
```

## 
## Want to help?

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

If someone want to helpme, every bit of effort will be appreciated. In [this link](https://github.com/agustinBassi/mq-connection/projects/1) there is the project status board. You can take any card you want (or propose one) from the ToDo list and start to work.

If you find it useful please helpme following my Github user and give to this project a Star. This will animate me to continue contribuiting with the great open source community.

## 
## License

This project is licensed under the GPLV3 License.

![footer](doc/footer.png)