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
MIN_SCAN_TICK          = 1
MAX_SCAN_TICK          = 10


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
        self._scan_thread         = None
        self._changes_callback    = None

    def run(self, fake_scan=False):
        if self._run_flag == False: # and self._scan_thread is None:
            logging.info("Starting to scan iBeacon")
            self._run_flag = True
            if fake_scan:
                self._scan_thread = Thread(target=self._scan_fake)
            else:
                self._scan_thread = Thread(target=self._scan)
            self._scan_thread.start()

    def stop(self):
        if self._run_flag == True: # and self._scan_thread is not None:
            logging.info("Stopping iBeacons scanner")
            self._run_flag = False
            # wait for thread to finalize
            self._scan_thread.join()

    def set_changes_callback(self, callback=None):
        if callback is not None:
            logging.info("Setting changes callback")
            self._changes_callback = callback
        else:
            logging.warn("Changes callback is invalid")

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
            # evaluate if nearest beacon has changes, if so, invoke changes callback
            if self._check_if_nearest_beacon_changes():
                self._invoke_changes_callback()

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
            # evaluate if nearest beacon has changes, if so, invoke changes callback
            if self._check_if_nearest_beacon_changes() and self._changes_callback is not None:
                self._invoke_changes_callback()

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

    def _check_if_nearest_beacon_changes(self):
        """ Checks if neares beacon has change in this new scan """
        if self._nearest_beacon is None and self._last_nearest_beacon is None:
            return False

        if self._nearest_beacon is None or self._last_nearest_beacon is None:
            return True
        
        if self._nearest_beacon.mac_address != self._last_nearest_beacon.mac_address:
            return True
        else:
            return False

    def _invoke_changes_callback(self):
        if self._changes_callback is not None:
            changes_data = {}
            changes_data["nearest_beacon"] = self.nearest_beacon
            logging.debug("Calling to changes callback")
            self._changes_callback(changes_data)

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

    def to_json(self):
        return json.loads(repr(self).replace("\'", "\""))
    
    def to_dict(self):
        return ast.literal_eval(repr(self))

    def to_str(self):
        return repr(self)

    def update_settings(self, settings=None):
        if isinstance(settings, str):
            # convert str to json dict
            settings = json.loads(settings)
        
        if isinstance(settings, dict):
            # Check if settings dict has uuid_filter property and validate it
            if settings.get("uuid_filter") is not None and \
                type(settings.get("uuid_filter")) == str:
                logging.debug("Updating uuid_filter")
                # TODO: A validator format must be applied here
                self._uuid_filter = settings.get("uuid_filter")
            # Check if settings dict has uuid_filter property and validate it
            if settings.get("scan_tick") is not None and \
                type(settings.get("scan_tick")) == int:
                logging.debug("Updating scan_tick")
                # validate if value is in correct range
                if settings.get("scan_tick") < MIN_SCAN_TICK:
                    settings["scan_tick"] = MIN_SCAN_TICK
                elif settings.get("scan_tick") > MAX_SCAN_TICK:
                    settings["scan_tick"] = MAX_SCAN_TICK
                # assing new scan tick
                self._scan_tick = settings.get("scan_tick")
            # Check if settings dict has uuid_filter property and validate it
            if settings.get("run_flag") is not None and \
                type(settings.get("run_flag")) == bool:
                self.run() if settings.get("run_flag") else self.stop()
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
        data_repr["run_flag"]            = self._run_flag

        return str(data_repr)


#########[ Module main code ]##################################################

def changes_callback(changes_data):
    logging.info("Nearest beacon has changed: " + str(changes_data))

def run_ibeacons_controller():
    print ("\n\nWelcome to iBeacons Reader - Powered by Agustin Bassi\n\n")
    # configure logging
    logging.basicConfig(
        format='[ %(levelname)5s ] - %(funcName)26s -> %(message)s',
        level=logging.DEBUG,
        datefmt='%H:%M:%S'
        )
    # beacons controller instance
    beacons_scanner = IBeaconsScanner(uuid_filter=DEFAULT_BEACONS_FILTER, scan_tick=DEFAULT_SCAN_TICK)
    beacons_scanner.set_changes_callback(changes_callback)
    # print current configuration
    # print(beacons_scanner)
    # start stanning for 10 seconds
    beacons_scanner.run()
    time.sleep(10)
    beacons_scanner.stop()
    # update settings and show them
    settings_dict = {'uuid_filter' : 'aa-bb-cc-dd-ee-ff', 'scan_tick' : 5 }
    beacons_scanner.update_settings(settings=settings_dict)
    # print(beacons_scanner)
    # start stanning for 10 seconds
    beacons_scanner.run()
    time.sleep(10)
    beacons_scanner.stop()

if __name__ == '__main__':
    run_ibeacons_controller()

#########[ TODO section ]######################################################

# TODO: Create a callback function into IBeaconScanner to advice it when nearest beacon changes
# TODO: Put ASCII into welcome message
# TODO: Put a flag run in settings

#########[ Enf of file ]#######################################################