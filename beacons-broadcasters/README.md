![banner](doc/banner.png)

# Beacons Broadcasters


Author: Agustin Bassi - 2020


## 

## Table of Contents


* [Description](#description)
* [iBeacon broadcast from Linux systems](#iBeacon-broadcast-from-linux-systems)
* [iBeacon broadcast from Android](#iBeacon-broadcast-from-android)
* [Contributing](#contributing)
* [License](#license)


# 
# Description

This section consists in be able to broadcast beacon packages from different platforms, like ESP32, Linux Systems or even any Bluetooth LE 4.0+ compatible smartphone. To broadcast any Bluetooth LE beacon package, a bluetooth le 4.0+ hardware is needed. 

# 
# iBeacon broadcast from Linux systems

This method describes how to install and broadcast iBeacon packeges from Linux systems using a python script.


## Install dependencies

The first thing needed is to install system dependencies with the commands below.

```
sudo apt-get update
sudo apt-get install bluetooth bluez-utils blueman
```

Once the packages are installed test to access to bluetooth hardware with the next command.

```
sudo hcitool lescan
```

If no error is shown in the terminal, or if there are near bluetooth devices, the output should be like as follows.

```
LE Scan ...
7B:C1:CD:0F:33:F2 (unknown)
7B:C1:CD:0F:33:F2 (unknown)
7B:C1:CD:0F:33:F2 (unknown)
7B:C1:CD:0F:33:F2 (unknown)
```

Stop the scans pressing CTRL+C.

## Run iBeacon broadcaster

In order to run the broadcaster at least Python 2.7 is needed. If not installed refer to [official documentation](https://python.org) to find installation procedure. The next step is to go to linux-ibeacon-broadcaster folder and execute the command below.

```
sudo python ibeacon_broadcaster.py --uuid=ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee --major=111 --minor=222
```

To stop iBeacon transmission, execute the next command.

```
sudo python ibeacon_broadcaster.py --down
```

To check more option pass to the script --help argument to see full options.

> **_Note:_**: To be sure that the frames are being sent correctly, enable beacons-observer as described in its [README.md](../beacons-observer/README.md) and position yourself within a radius of less than 10 meters with the beacon emitter and check if the scanner is capable of taking the corresponding readings.

# 
# iBeacon broadcast from Android

This method is really simple and only consists to download and configure the Beacon Simulator Android application.

Follow the steps in the table below.

| Step | Description   | Image |
| ---- | ------------- | ----- |
| **_1_** | Download Beacon Simulator from app store   | ![1](doc/android_1.png) |
| **_2_** | Activate the Bluetooth and open the application   | ![2](doc/android_2.png) |
| **_3_** | Press '+' icon and choose iBeacon option | ![3](doc/android_3.png) |
| **_4_** | Create iBeacon with the next configurations. [name: iBeacon1 - uuid:ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee - major:111 - minor: 222] | ![4](doc/android_4.png) |
| **_5_** | Finally, enable iBeacon switch to starting to boradcast iBeacon packages | ![5](doc/android_5.png) |

> **_Note:_**: To be sure that the frames are being sent correctly, enable beacons-observer as described in its [README.md](../beacons-observer/README.md) and position yourself within a radius of less than 10 meters with the beacon emitter and check if the scanner is capable of taking the corresponding readings.




# 
# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

# 
# License

This project is licensed under the GPLV3 License.

If you find it useful please helpme with follow to my Github user and mark this project with a Star. This will animate me to continue contribuiting with the great open source community.