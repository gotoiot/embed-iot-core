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
        return "{} - (MAC={}, UUID={}, MAJOR={}, MINOR={}, TXP={}, RSSI={})".format(
            self.__class__.__name__,
            self.mac_address, 
            self.uuid[:6], 
            self.major, 
            self.minor, 
            self.tx_power, 
            self.rssi
            )

    def serialize(self):
        return "{ 'mac':'{}', 'uuid':'{}', 'major':'{}', 'minor':'{}', 'txp':'{}', 'rssi':'{}' }".format(
            self.mac_address, 
            self.uuid[:6], 
            self.major, 
            self.minor, 
            self.tx_power, 
            self.rssi
            )


class IBeaconsScanner:

    #####[ Public methods ]################################

    def __init__(self, uuid_filter=DEFAULT_BEACONS_FILTER, scan_tick=DEFAULT_SCAN_TICK):
        """ Init this class that controls the beacons reads """
        self._beacons_list = []
        self._uuid_filter = uuid_filter
        self._scan_tick = scan_tick
        self.__nearest_beacon = IBeacon("", "", 0, 0, 0, 0)
        self.__last_nearest_beacon = self.__nearest_beacon
        self.__run_flag = False

    def run(self, fake_scan=False):
        logging.info("Starting to scan iBeacon")
        self.__run_flag = True
        if fake_scan:
            scan_thread = Thread(target=self._scan_fake)
        else:
            scan_thread = Thread(target=self._scan)
        scan_thread.start()

    def stop(self):
        logging.info("Stopping iBeacons scanner")
        self.__run_flag = False

    def is_nearest_beacon_change(self):
        """ Checks if neares beacon has change recently """
        if 	self.__nearest_beacon.major != self.__last_nearest_beacon.major or \
            self.__nearest_beacon.minor != self.__last_nearest_beacon.minor:
            return True
        return False

    #####[ Protected methods ]#############################
    
    def _scan(self):
        """ This function scans for iBeacon packets, save them in a list, 
        order packets by RSSI and update near beacons attrs accordingly """
        def _scans_callback(bt_addr, rssi, packet, additional_info):
            beacon = IBeacon(bt_addr, packet.uuid, packet.major, packet.minor, packet.tx_power, rssi)
            if not self._is_beacon_in_list(beacon):
                self._beacons_list.append(beacon)
        
        while(self.__run_flag):
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
                self.__last_nearest_beacon = self.__nearest_beacon
                self.__nearest_beacon = self._beacons_list[0]
                logging.info("Nearest beacon: {}".format(self.__nearest_beacon))
            else:
                self.__last_nearest_beacon = self.__nearest_beacon
                self.__nearest_beacon = None
                logging.info("No beacons found in this scan")

    def _scan_fake(self):
        """ emulates the behaviour of update() """
        import random
        # clear list
        self._beacons_list = []
        # append some beacons to list
        self._beacons_list.append(IBeacon("11:11:11", DEFAULT_BEACONS_FILTER, 11, 1, -50, random.randint(1, 100) * -1))
        self._beacons_list.append(IBeacon("22:22:22", DEFAULT_BEACONS_FILTER, 11, 2, -50, random.randint(1, 100) * -1))
        self._beacons_list.append(IBeacon("33:33:33", DEFAULT_BEACONS_FILTER, 11, 3, -50, random.randint(1, 100) * -1))
        # order the beacons list by RSSI (Power received)
        if len(self._beacons_list) >= 1:
            self._order_beacons_list()
            self.__last_nearest_beacon = self.__nearest_beacon
            self.__nearest_beacon = self._beacons_list[0]
            logging.info("Nearest beacon: {}".format(self.__nearest_beacon))
        else:
            self.__last_nearest_beacon = self.__nearest_beacon
            self.__nearest_beacon = None
            logging.warn("No beacons found in this scan")

    def _is_beacon_in_list(self, beacon):
        """ Check if a beacons is in the current beacons list """
        for beacon_item in self._beacons_list:
            if beacon_item.major == beacon.major and beacon_item.minor == beacon.minor:
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
        return self.__nearest_beacon

    @property
    def last_nearest_beacon(self):
        return self.__last_nearest_beacon

    @property
    def beacons_list(self):
        return self._beacons_list

    #####[ Dunderscore methods ]###########################

    def __str__(self):
        return "{} ('uuid_filter': '{}', 'scan_tick': '{}')".format(
            self.__class__.__name__, self._uuid_filter, self._scan_tick)

    def __repr__(self):
        return "{ 'uuid_filter': '{}', 'scan_tick': '{}' }".format(
            self._uuid_filter, self._scan_tick)


#########[ Module main code ]##################################################

def run_ibeacons_controller():
    print ("Welcome to iBeacons Reader - Powered by Agustin Bassi")
    # configure logging
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
        datefmt='%H:%M:%S'
        )
    # beacons controller instance
    beacons_scanner = IBeaconsScanner(
        uuid_filter=DEFAULT_BEACONS_FILTER, 
        scan_tick=DEFAULT_SCAN_TICK
        )
    
    beacons_scanner.run()
    time.sleep(15)
    beacons_scanner.stop()

    
if __name__ == '__main__':
    run_ibeacons_controller()

#########[ Enf of file ]#######################################################
