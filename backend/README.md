# BLUE Connection - Beacons Reader



Author: Agustin Bassi - 2020



# Table of Contents



* [Application description](#application-description)
* [Install dependencies](#install-dependencies)
* [Test beacons scanning](#test-beacons-scanning)
* [Run the application](#run-the-application)
* [Available HTTP resources](#available-http-resources)
* [Test the project](#test-the-project)



# Application description



This application consists in a Beacons Scanner. The function of the scanner is to look for beacons packages, which could be iBeacons, Eddystone and others. 

> **_NOTE:_**  The available support is only for iBeacons currently.

The app can works as standalone app (it means it can runs from CLI and scan for Beacons) or working together with an HTTP server made in Flask Web Framework, which can GET & PUT data into the scanner. 

By this way the scanner can be consulted for nearest beacons, last nearest beacons, list of beacons read and others, or even be modified by an HTTP client through, for example configure beacon filters, scan time, or turn on/off the scanner.

This application is composed with the next relevant parts:

* `src/app.py`: Flask application with HTTP API handlers and database handling (reading & writing to file in JSON format).
* `src/beacons/`: Package containing several software modules used for scan and control different beacons packages. The modules in this package can be used solely without integration with Flask API.
* `db/db.json`: DB file with module configuration in JSON format, to be simple to read from and write to using the support of standard Python library.

> **_TODO:_**  Document the secuence to configure an URI callback



# Install dependencies



This application runs in Linux systems with integrated Bluetooth, like the most modern laptops or in Raspberry Pi 3+.

The requirements to run the application are:

* Get integrated Bluetooth hardware.
* Python 3.x.
* Docker (optional).

The first step is to install Python 3.x. If not installed refer to [official documentation](https://python.org) to find installation procedure.


## Install Bluetooth packages


In order to install dependencies for Bluetooth and grant access to Python to system Bluetooth HW execute the next commands.

```
sudo apt-get install -y libbluetooth-dev libcap2-bin
sudo setcap 'cap_net_raw,cap_net_admin+eip' $(readlink -f $(which python))
```

Then install Python Bluetooth packages which allows to read beacons from script.

```
sudo pip install beacontools[scan]
sudo pip install beacontools
```

> **_NOTE:_**  Due to the Python packages need to access to system hardware, they must be installed globally.


# Test beacons scanning


Before to run the application is prefereable to test the if beacons packages can be read. To do that, go to src/beacons and run any python script which starts with `test_###.py`.

Also is nice to have a beacon emitting packages in order to read them, but if not, only test if the dependencies are correctly installed running the test script.

As an example, running the test_ibeacon_scanner.py show an output like this.

```
Starting to scan beacons with UUID=ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee for 10 seconds

[MAC: 28:c6:3f:7c:5c:26 | RSSI: -58 ] <id: ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee, M: 13, m: 12>
[MAC: 28:c6:3f:7c:5c:26 | RSSI: -58 ] <id: ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee, M: 13, m: 12>
[MAC: 28:c6:3f:7c:5c:26 | RSSI: -58 ] <id: ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee, M: 13, m: 12>

Scan beacons finished!
```



# Run the application



The system can runs as system Python application or in a Docker container. Choose the method and follow the steps in each case.


## Python application within Virtual Environment


To run in this mode, at first create & activate the Python Virtual Environment with the commands below. By default this commands will create a venv in the `current_directory/.venv` (supposed to be in the project root folder, where this README is), but you can change it for any path you want.

```sh
python3 -m venv "$PWD"/.venv
source "$PWD"/.venv/bin/activate
```

Once venv is activated execute the command below to install project dependencies.

```sh
pip install -r src/requirements.txt
```

To run the project, simply execute the next command.

```sh
python3 src/app.py
```


## Docker container


This option is prefereable in the majority of cases, because this application can be a part of a larger application. Besides, using Docker you garantee that project can be reproducible in any scenario with the same easy steps.

The first step is to build the Docker image which has all project dependencies bundled in it. Execute the next command.

```
docker build --tag local/beacons-scanner .
```

> **_NOTE:_**: You can build your image with `prod` tag putting your code into the image once you have your code finished. Read the Dockerfile to change from `dev` to `prod`.

The command above will create the image. You will see an output like the next.

```
Sending build context to Docker daemon  19.48MB
Step 1/9 : FROM python:3
 ---> 659f826fabf4
 ...
 ---> fed022191ead
Successfully built fed022191ead
Successfully tagged local/beacons-reader:latest
```

Finally run the application Docker container. In the project root folder (where this README is) run the next command.

```
docker run \
--rm \
--interactive \
--name beacons-scanner \
--net host \
--publish 5001:5000 \
--volume "$PWD"/db:/app/db \
--volume "$PWD"/src:/app/src \
local/beacons-scanner:latest \
python app.py
```

In the command above you are running the Docker container with name `beacons-scanner`, running the container in `host` network (to enable access to bluetooth access), binding your host port 5001 into container port 5000, sharing the application db path (`"$PWD"/db`) into container db path (`/app/db`), sharing your source code folder (`"$PWD"/src`) into container source folder (`/app/src`), and running the `app.py` with python when container starts.

Alternative, you can run the application executing `run_ibeacon_scanner.sh` in the root folder as follows, that will be the same as previous long docker command:

```
./run_ibeacon_scanner.sh "$PWD"/src app.py "$PWD"/db 5001 host
```



# Available HTTP resources



The available HTTP resources for the application API are the described below.

Get the available resources from client

| Description     | Value |
| -------------   | ------------- |
| URI             | http://localhost:5000/api/v1/  |
| METHOD          | GET  |
| Details         | Obtain the URLs for available resources  |
| Request Header  | Accept: application/json - Content-Type: application/json  |
| Request body    | - |
| Response body   | { {"ibeacons_info": {"url_get": "..."}, "ibeacons_settings": {"url_get": "...", "url_post": "...", "url_put": "..."}, "interface_settings": {"url_get": "...", "url_post": "...", "url_put": "..."}} }  |

Get scanner settings

| Description     | Value |
| -------------   | ------------- |
| URI             | http://localhost:5000/api/v1/ibeacons_settings/  |
| METHOD          | GET  |
| Details         | Obtain the current scanner settings in JSON Format. Returns all current settings  |
| Request Header  | Accept: application/json - Content-Type: application/json  |
| Request body    | - |
| Response body   | { "run_flag": false, "scan_tick": 4, "uuid_filter": "aa-bb-cc-dd-ee-ff" }  |

Set scanner settings

| Description     | Value |
| -------------   | ------------- |
| URI             | http://localhost:5000/api/v1/ibeacons_settings/  |
| METHOD          | POST, PUT  |
| Details         | Set the current scanner settings in JSON Format. Returns all current settings  |
| Request Header  | Accept: application/json - Content-Type: application/json  |
| Request body    | { "run_flag": true, "scan_tick": 3, "uuid_filter": "aa-bb-cc-dd-ee-ff" } |
| Response body   | Same as request received  |

Get scanner info 

| Description     | Value |
| -------------   | ------------- |
| URI             | http://localhost:5000/api/v1/ibeacons_info/ |
| METHOD          | GET  |
| Details         | Obtain the current scanner information, like nearest beacon and beacons list. Returns info in JSON format  |
| Request Header  | Accept: application/json - Content-Type: application/json  |
| Request body    | - |
| Response body   | {"beacons_list": [], "last_nearest_beacon": {"mac_address": "", "major": 0, "minor": 0, "rssi": 0, "tx_power": 0, "uuid": ""}, "nearest_beacon": {"mac_address": "", "major": 0, "minor": 0, "rssi": 0, "tx_power": 0, "uuid": ""}, "run_flag": false, "scan_tick": 4, "uuid_filter": "ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee"}  |

Get application interface settings

| Description     | Value |
| -------------   | ------------- |
| URI             | http://localhost:5000/api/v1/interface_settings/  |
| METHOD          | GET  |
| Details         | Obtain the application interfaces settings.  |
| Request Header  | Accept: application/json - Content-Type: application/json  |
| Request body    | - |
| Response body   | { "callback_uri": "https://host:port/api/for/callback" }  |

Get application interface settings

| Description     | Value |
| -------------   | ------------- |
| URI             | http://localhost:5000/api/v1/interface_settings/  |
| METHOD          | POST, PUT  |
| Details         | Set the application interfaces settings.  |
| Request Header  | Accept: application/json - Content-Type: application/json  |
| Request body    | { "callback_uri": "https://host:port/api/for/callback" } |
| Response body   | Same as request received  |



# Test the HTTP API interface



The easy and best way to test the project is using [Postman](https://www.postman.com/), a really intuitive and easy to use tool for execute HTTP methods.

If you decide to quickly test the project you can use `curl`. In the next snippets is shown how to test each project resource.


Get available resources

```
curl -i \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-X GET \
http://localhost:5000/api/v1/
```

Get module settings

```
curl -i \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-X GET \
http://localhost:5000/api/v1/ibeacon_settings/
```

Add or change a key in module settings.

```
curl -i \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-X POST \
--data '{ "run_flag": false, "scan_tick": 4, "uuid_filter": "aa-bb-cc-dd-ee-ff" }' \
http://localhost:5000/api/v1/ibeacon_settings/
```

Get ibeacon info

```
curl -i \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-X GET \
http://localhost:5000/api/v1/ibeacons_info/
```

Get interface settings

```
curl -i \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-X GET \
http://localhost:5000/api/v1/interface/
```

Add or change a key in interface settings.

```
curl -i \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-X POST \
--data '{ "callback_uri": "https://host:port/api/for/callback" }' \
http://localhost:5000/api/v1/interface/
```


# Contributing



Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

If you find it useful please helpme with follow to my Github user and a Star project, it will animate me to continue contribuiting with the great open source community.



# Licence



GPLV3
