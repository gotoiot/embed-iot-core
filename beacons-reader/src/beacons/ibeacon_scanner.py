#!/usr/bin/python
###############################################################################
# Author: Agustin Bassi
# Date: June 2020
# Licence: GPLV3
# Brief: iBeacons scanner. In order to scan properly an iBeacon device 
# must be near of this scanner and transmitting its packages.
###############################################################################

#########[ Imports ]########################################################### 

import logging
import subprocess
import time
from threading import Thread
import json
import ast

from beacontools import BeaconScanner
from beacontools import IBeaconFilter

#########[ Settings & Data ]###################################################

DEFAULT_SCAN_TICK      = 3	
DEFAULT_BEACONS_FILTER = "ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee"

#########[ Module Classes ]####################################################

class IBeacon:

    def __init__(self, mac_address, uuid, major, minor, tx_power, rssi):
        """ Class that represents an iBeacon packet """
        self.mac_address = mac_address
        self.uuid = uuid
        self.major = major
        self.minor = minor
        self.tx_power = tx_power
        self.rssi = rssi		

    def __str__(self):
        return repr(self)

    def __repr__(self):
        data_repr = {}
        data_repr["mac_address"] = self.mac_address
        data_repr["uuid"]        = self.uuid
        data_repr["major"]       = self.major
        data_repr["minor"]       = self.minor
        data_repr["tx_power"]    = self.tx_power
        data_repr["rssi"]        = self.rssi
        return str(data_repr)


class IBeaconsScanner:

    #####[ Public methods ]################################

    def __init__(self, uuid_filter=DEFAULT_BEACONS_FILTER, scan_tick=DEFAULT_SCAN_TICK):
        """ Init this class that controls the beacons reads """
        self._beacons_list        = []
        self._uuid_filter         = uuid_filter
        self._scan_tick           = scan_tick
        self._nearest_beacon      = IBeacon("", "", 0, 0, 0, 0)
        self._last_nearest_beacon = self._nearest_beacon
        self._run_flag            = False

    def run(self, fake_scan=False):
        logging.info("Starting to scan iBeacon")
        self._run_flag = True
        if fake_scan:
            scan_thread = Thread(target=self._scan_fake)
        else:
            scan_thread = Thread(target=self._scan)
        scan_thread.start()

    def stop(self):
        # TODO: the thread can be stopped as well
        logging.info("Stopping iBeacons scanner")
        self._run_flag = False

    def is_nearest_beacon_change(self):
        """ Checks if neares beacon has change recently """
        return True if self._nearest_beacon.mac_address != self._last_nearest_beacon.mac_address else False

    #####[ Protected methods ]#############################
    
    def _scan(self):
        """ This function scans for iBeacon packets, save them in a list, 
        order packets by RSSI and update near beacons attrs accordingly """
        def _scans_callback(bt_addr, rssi, packet, additional_info):
            beacon = IBeacon(bt_addr, packet.uuid, packet.major, packet.minor, packet.tx_power, rssi)
            if not self._is_beacon_in_list(beacon):
                self._beacons_list.append(beacon)
        
        while(self._run_flag):
            # clear beacon list
            self._beacons_list = []
            # instance the scanner
            scanner = BeaconScanner(
                _scans_callback, 
                device_filter=IBeaconFilter(uuid=self._uuid_filter)
            )
            # perform the scan
            scanner.start()
            time.sleep(self._scan_tick)
            scanner.stop()
            # order the beacons list by RSSI (Power received)
            if len(self._beacons_list) >= 1:
                self._order_beacons_list()
                self._last_nearest_beacon = self._nearest_beacon
                self._nearest_beacon = self._beacons_list[0]
                logging.info("Nearest beacon: {}".format(self._nearest_beacon))
            else:
                self._last_nearest_beacon = self._nearest_beacon
                self._nearest_beacon = None
                logging.info("No beacons found in this scan")

    def _scan_fake(self):
        """ emulates the behaviour of update() """
        import random

        while(self._run_flag):
            # clear list
            self._beacons_list = []
            # append some beacons to list
            self._beacons_list.append(IBeacon("11:11:11", DEFAULT_BEACONS_FILTER, 11, 1, -50, random.randint(1, 100) * -1))
            self._beacons_list.append(IBeacon("22:22:22", DEFAULT_BEACONS_FILTER, 11, 2, -50, random.randint(1, 100) * -1))
            self._beacons_list.append(IBeacon("33:33:33", DEFAULT_BEACONS_FILTER, 11, 3, -50, random.randint(1, 100) * -1))
            # order the beacons list by RSSI (Power received)
            if len(self._beacons_list) >= 1:
                self._order_beacons_list()
                self._last_nearest_beacon = self._nearest_beacon
                self._nearest_beacon = self._beacons_list[0]
                logging.info("Nearest beacon: {}".format(self._nearest_beacon))
            else:
                self._last_nearest_beacon = self._nearest_beacon
                self._nearest_beacon = None
                logging.warn("No beacons found in this scan")

    def _is_beacon_in_list(self, beacon):
        """ Check if a beacons is in the current beacons list """
        for beacon_item in self._beacons_list:
            if beacon_item.mac_address == beacon.mac_address:
                return True
        return False

    def _order_beacons_list(self, oderType=None):
        """ Order function by some orderType """
        self._beacons_list = sorted(
            self._beacons_list, 
            key = lambda beacon : beacon.rssi, 
            reverse = True
            )

    #####[ Getters & Setters ]#############################

    @property
    def nearest_beacon(self):
        return self._nearest_beacon

    @property
    def last_nearest_beacon(self):
        return self._last_nearest_beacon

    @property
    def beacons_list(self):
        return self._beacons_list

    def _to_json(self):
        return json.loads(repr(self).replace("\'", "\""))
    
    def _to_dict(self):
        return ast.literal_eval(repr(self))

    def _to_str(self):
        return repr(self)

    def update_settings(self, settings=None):
        if isinstance(settings, str):
            print("Convert str to dict")
            # convert str to json dict
            settings = json.loads(settings)
        
        if isinstance(settings, dict):
            # Check if settings dict has uuid_filter property and validate it
            if settings.get("uuid_filter") and \
                type(settings.get("uuid_filter")) == str:
                logging.info("Updating uuid_filter")
                self._uuid_filter = settings.get("uuid_filter")
            # Check if settings dict has uuid_filter property and validate it
            if settings.get("scan_tick") and \
                type(settings.get("scan_tick")) == int:
                logging.info("Updating scan_tick")
                self._scan_tick = settings.get("scan_tick")
        else:
            logging.warn("Invalid settings format")
        
    #####[ Dunderscore methods ]###########################

    def __str__(self):
        return repr(self)

    def __repr__(self):
        data_repr = {}
        data_repr["uuid_filter"]         = self._uuid_filter
        data_repr["scan_tick"]           = self._scan_tick
        data_repr["nearest_beacon"]      = self.nearest_beacon
        data_repr["last_nearest_beacon"] = self.last_nearest_beacon
        data_repr["beacons_list"]        = self.beacons_list

        return str(data_repr)


#########[ Module main code ]##################################################

def run_ibeacons_controller():
    print ("Welcome to iBeacons Reader - Powered by Agustin Bassi")
    # configure logging
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        datefmt='%H:%M:%S'
        )
    # beacons controller instance
    beacons_scanner = IBeaconsScanner(uuid_filter=DEFAULT_BEACONS_FILTER, scan_tick=DEFAULT_SCAN_TICK)
    # print current configuration
    print(beacons_scanner)
    # start stanning for 10 seconds
    beacons_scanner.run()
    time.sleep(10)
    beacons_scanner.stop()
    # update settings and show them
    settings_dict = {'uuid_filter' : 'aa-bb-cc-dd-ee-ff', 'scan_tick' : 5 }
    beacons_scanner.update_settings(settings=settings_dict)
    print(beacons_scanner)
    # start stanning for 10 seconds
    beacons_scanner.run()
    time.sleep(10)
    beacons_scanner.stop()

if __name__ == '__main__':
    run_ibeacons_controller()

#########[ TODO section ]######################################################

# TODO: Create a callback function into IBeaconScanner to advice it when nearest beacon changes
# TODO: Put ASCII into welcome message

#########[ Enf of file ]#######################################################