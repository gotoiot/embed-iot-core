# Raspberry Pi Beacons Reader Kiosk

Author: Agustin Bassi - 2020

# Description

The project consists in a Raspberry Pi that is constantly reading near Bluetooth LE Beacons. Once the nearest beacon is readed, the application sends the beacon ID to CMS as a request, and the CMS respond with a targetized content to show in a screen connected to Raspberry Pi depending on which beacon is the nearest.

It implies that it can show targetized content depending on the context, and whole content shown in the screen depends on CMS System and the Raspberry Pi acts as a fool terminal.

The application workflow looks as follow:

![app workflow](./doc/workflow.png)

> **_NOTE:_**  The CMS System is not included in this project because it can works with any of the available CMS in the market.


# Beacons Reading from Raspberry Pi

In this section its shown to configure Raspberry Pi for beacons reading.

## Raspberry Pi OS Installation

The first step is to download the Raspberry Pi OS from [oficial web page](https://www.raspberrypi.org/downloads/). You can follow my instruction document to install and configure Raspberry Pi OS in this link.


## Configure browser as kiosk

The best browser to perform this action is Iceweasel, which allows to update their content always in the same tab (with a configuration settings). Other ones, does not allow that, and every time the content changes, a new tab is open, increasing the RAM and processor consume.

Starting by downloading the browser with the command below.

```
sudo apt-get install iceweasel
```

Once it is installed, open it and write `about:config` in navigation bar to open up the settings. Modify the next lines with this values.

```
browser.link.open_newwindow.restriction=0 (default 2)
browser.link.open_newwindow = 1 (default 3)
```

To show the content in full screen (kiosk mode) as default, install the Add-On "R-Kiosk" in the Addons section.

To test it, from terminal type the command below, it must show Google page in full screen mode.

```
iceweasel www.google.com
```

## Install Bluetooth packages

In order to install dependencies for Bluetooth execute the next commands.

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

## Test beacons reading

To test that beacons packages are working fine in the Raspberry Pi create a python script with the content below.


```python
import argparse
import time

from beacontools import BeaconScanner
from beacontools import IBeaconFilter

DEFAULT_TIME_TO_SCAN = 10
DEFAULT_BEACON_UUID  = "ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee"

def scan_beacons():
   # callback to show beacons read
   def callback(bt_addr, rssi, packet, additional_info):
       print("[ MAC: {} | RSSI: {} ] - {}".format(bt_addr, rssi, packet))
   # intance the parser
   parser = argparse.ArgumentParser()
   parser.add_argument('-u', '--uuid', action='store', dest='uuid',
                       help='iBeacon UUID. Def: {}'.format(DEFAULT_BEACON_UUID))
   parser.add_argument('-t', '--time', action='store', dest='scan_time', type=float,
                       help='Scan time. Def: {}'.format(DEFAULT_TIME_TO_SCAN))
   # get result of parse arguments in 'r'
   res = parser.parse_args()
   uuid = res.uuid if res.uuid is not None else DEFAULT_BEACON_UUID
   scan_time = res.scan_time if res.scan_time is not None else DEFAULT_TIME_TO_SCAN
   # scan for all iBeacon advertisements from beacons with the specified uuid
   scanner = BeaconScanner(callback, device_filter=IBeaconFilter(uuid=uuid))
   # start scanning
   print ("Starting to scan beacons with UUID={} for {} seconds".format(uuid, scan_time))
   scanner.start()
   time.sleep(scan_time)
   scanner.stop()
   print ("Scan beacons finished!")

if __name__ == "__main__":
   scan_beacons()
```

To run the script ensure that beacon emiter with the UUID "ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee" is sending beacon packages in 10 meters around the Raspberry Pi. Run the script and the output must look like follows:


```
Starting to scan beacons with UUID=ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee for 10 seconds

[MAC: 28:c6:3f:7c:5c:26|RSSI: -58 ] <id: ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee, M: 13, m: 12>

[MAC: 28:c6:3f:7c:5c:26|RSSI: -58 ] <id: ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee, M: 13, m: 12>

[MAC: 28:c6:3f:7c:5c:26|RSSI: -58 ] <id: ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee, M: 13, m: 12>

Scan beacons finished!
```

## Run the application code

Once the beacon reading is working OK, run the application with the command below:

```
python beacon_scanner.py
```

The script must open the browser automatically and must start to show information related to beacons. The command output should look like the next.

```

Welcome to Rpi Beacons Kiosk - Powered by Agustin Bassi
16:11:21 - INFO - BeaconsController ('uuid_filter': 'ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee', 'scan_tick': '3')
16:11:21 - INFO - WebController - ('cms_ip':'192.168.0.172', 'cms_port': '8080', 'cms_resource': 'beacons')
16:11:21 - INFO - Nearest beacon: Beacon - (MAC=33:33:33, UUID=ffffff, MAJOR=11, MINOR=3, TXP=-50, RSSI=-67)
16:11:21 - INFO - Invoking URL: http://192.168.0.172:8080/beacons?major=11&minor=3
16:11:24 - INFO - Nearest beacon: Beacon - (MAC=22:22:22, UUID=ffffff, MAJOR=11, MINOR=2, TXP=-50, RSSI=-31)
```

# Contributing


Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


# License

[GPL]


