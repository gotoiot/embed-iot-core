#!/usr/bin/python
###############################################################################
# Author: Agustin Bassi
# Date: June 2020
# Licence: GPLV3
# Brief: Simple iBeacons scanner to test if the hardware is properly configred
# and can execute correct reads. In order to scan properly an iBeacon device 
# must be near of this scanner and transmitting its packages.
###############################################################################

#########[ Imports ]########################################################### 

import argparse
import time

from beacontools import BeaconScanner
from beacontools import IBeaconFilter

#########[ Settings & Data ]###################################################

DEFAULT_TIME_TO_SCAN = 10
DEFAULT_BEACON_UUID  = "ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee"

#########[ Module main code ]##################################################

def scan_ibeacons():
	# callback to show beacons read
	def callback(bt_addr, rssi, packet, additional_info):
		print("[ MAC: {} | RSSI: {} ] - {}".format(bt_addr, rssi, packet))
	# intance the parser
	parser = argparse.ArgumentParser()
	# parse uuid argument
	parser.add_argument(
		'--uuid', 
		action='store', 
		dest='uuid',
		help='iBeacon UUID. Def: {}'.format(DEFAULT_BEACON_UUID)
		)
	# parse scan_time argument
	parser.add_argument(
		'--time', 
		action='store', 
		dest='scan_time',
		help='Scan time. Def: {}'.format(DEFAULT_TIME_TO_SCAN)
		)
	# get result of parse arguments in args
	args = parser.parse_args()
	uuid = args.uuid if args.uuid is not None else DEFAULT_BEACON_UUID
	scan_time = args.scan_time if args.scan_time is not None else DEFAULT_TIME_TO_SCAN
	# scan for all iBeacon advertisements from beacons with the specified uuid
	scanner = BeaconScanner(callback, device_filter=IBeaconFilter(uuid=uuid))
	# start scanning
	print ("Starting to scan beacons with UUID={} for {} seconds".format(uuid, scan_time))
	scanner.start()
	time.sleep(scan_time)
	scanner.stop()
	print ("Scan beacons finished!")

if __name__ == "__main__":
	scan_ibeacons()

#########[ Enf of file ]#######################################################
