# Beacon Scanner and Kiosk application for Raspberry Pi
# Author: Agustin Bassi
# Date: August 2019
# Copyright: Agustin Bassi - 2019 
# ======= [Imports] ===========================================================

import time
import subprocess

from beacontools import BeaconScanner
from beacontools import IBeaconFilter

# ======= [APP Settings] ======================================================

APP_TICK       = 3 
SCAN_TICK      = 3	
BEACONS_FILTER = "ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee"
CMS_IP         = "192.168.0.172"
CMS_PORT       = 8080
CMS_RESOURCE   = "beacons"

# ======= [APP Classes] =======================================================

class Beacon:

	def __init__(self, mac_address, uuid, major, minor, tx_power, rssi):
		""" Class that represents an iBeacon packet """
		self.mac_address = mac_address
		self.uuid = uuid
		self.major = major
		self.minor = minor
		self.tx_power = tx_power
		self.rssi = rssi		

	def __str__(self):
		return "(MAC={}, UUID={}, MAJOR={}, MINOR={}, TXP={}, RSSI={})".format(
			self.mac_address, 
			self.uuid[:6], 
			self.major, 
			self.minor, 
			self.tx_power, 
			self.rssi
			)


class BeaconsController:

	def __init__(self, uuid_filter=BEACONS_FILTER, scan_tick=SCAN_TICK):
		""" Init this class that controls the beacons reads """
		self._beacons_list = []
		self._uuid_filter = uuid_filter
		self._scan_tick = scan_tick
		self.__nearest_beacon = Beacon("", "", 0, 0, 0, 0)
		self.__last_nearest_beacon = self.__nearest_beacon

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

	def update(self):
		""" This function scans for iBeacon packets, save them in a list, 
		order packets by RSSI and update near beacons attrs accordingly """
		def _scans_callback(bt_addr, rssi, packet, additional_info):
			beacon = Beacon(bt_addr, packet.uuid, packet.major, packet.minor, packet.tx_power, rssi)
			if not self._is_beacon_in_list(beacon):
				self._beacons_list.append(beacon)
		# clear beacon list
		self._beacons_list = []
		# instance the scanner
		scanner = BeaconScanner(
			_scans_callback, 
			device_filter = IBeaconFilter(uuid=self._uuid_filter)
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
			print ("Nearest beacon: {}".format(self.__nearest_beacon))
		else:
			self.__last_nearest_beacon = self.__nearest_beacon
			self.__nearest_beacon = None
			print("No beacons found in this scan")

	def update_fake(self):
		""" emulates the behaviour of update() """
		import random
		# clear list
		self._beacons_list = []
		# append some beacons to list
		self._beacons_list.append(Beacon("11:11:11", BEACONS_FILTER, 11, 1, -50, random.randint(1, 100) * -1))
		self._beacons_list.append(Beacon("22:22:22", BEACONS_FILTER, 11, 2, -50, random.randint(1, 100) * -1))
		self._beacons_list.append(Beacon("33:33:33", BEACONS_FILTER, 11, 3, -50, random.randint(1, 100) * -1))
		# order the beacons list by RSSI (Power received)
		if len(self._beacons_list) >= 1:
			self._order_beacons_list()
			self.__last_nearest_beacon = self.__nearest_beacon
			self.__nearest_beacon = self._beacons_list[0]
			print ("Nearest beacon: {}".format(self.__nearest_beacon))
		else:
			self.__last_nearest_beacon = self.__nearest_beacon
			self.__nearest_beacon = None
			print("No beacons found in this scan")

	def is_nearest_beacon_change(self):
		""" Checks if neares beacon has change recently """
		if 	self.__nearest_beacon.major != self.__last_nearest_beacon.major or \
			self.__nearest_beacon.minor != self.__last_nearest_beacon.minor:
			return True
		return False

	@property
	def nearest_beacon(self):
		return self.__nearest_beacon

	@property
	def last_nearest_beacon(self):
		return self.__last_nearest_beacon

	@property
	def beacons_list(self):
		return self._beacons_list

	def __str__(self):
		return "BeaconsController ('uuid_filter': '{}', 'scan_tick': '{}')".format(
			uuid_filter, scan_tick)


class WebController:

	def __init__(self, cms_ip=CMS_IP, cms_port=CMS_PORT, cms_resource=CMS_RESOURCE):
		""" Init the web controller. This class controls the content over web browser """
		self.cms_ip = cms_ip
		self.cms_port = cms_port
		self.cms_resource = cms_resource

	def update_content(self, arguments):
		""" Perform a HTTP GET request and send its content to browser """
		url = "http://{}:{}/{}?{}".format(self.cms_ip, self.cms_port, 
										  self.cms_resource, arguments)
		print ("Invoking URL: {}".format(url))
		process = subprocess.Popen(["iceweasel", url])
	
	def update_content_fake(self, arguments):
		""" Logs the content that will be sent to browser """
		url = "http://{}:{}/{}?{}".format(self.cms_ip, str(self.cms_port), 
											self.cms_resource, arguments)
		print ("Invoking URL: " + url)

	def __str__(self):
		return "WebController ('cms_ip':'{}', 'cms_port': '{}', 'cms_resource': '{}')".format(
			cms_ip, cms_port, cms_resource)


class AppController:

	def __init__(self, beacons_controller=None, web_controller=None, app_tick=APP_TICK):
		""" Init controllers and establish the application tick """
		self.app_tick = app_tick
		self.beacons_controller = beacons_controller
		self.web_controller = web_controller

	def __format_http_arguments(self, beacon):
		""" Receives a beacon and create string to send to http arguments """
		http_arguments = "major={}&minor={}".format(beacon.major, beacon.minor)
		return http_arguments

	def run(self):
		""" Main loop that runs forever. Read nearest beacon and update web content """
		while (True):
			# read near beacons
			self.beacons_controller.update_fake()
			# check if nearest beacon has changed against last near beacon
			if self.beacons_controller.is_nearest_beacon_change():
				# format argument to invoke URL with parameters
				http_arguments = self.__format_http_arguments(self.beacons_controller.nearest_beacon)
				# update the content in web navegator
				self.web_controller.update_content_fake(http_arguments)
			time.sleep(self.app_tick)

# ======= [Main function] =====================================================

def main ():
	""" Main function. Instance needed classes and run AppController loop """
	print ("Welcome to Rpi Beacons Kiosk - Powered by Agustin Bassi")
	# beacons controller instance
	beacons_controller = BeaconsController(
		uuid_filter=BEACONS_FILTER, 
		scan_tick=SCAN_TICK
		)	
	# web controller instance
	web_controller = WebController(
		cms_ip=CMS_IP, 
		cms_port=CMS_PORT, 
		cms_resource=CMS_RESOURCE
		)
	# app controller instance
	app_controller = AppController(
		beacons_controller=beacons_controller, 
		web_controller=web_controller,
		app_tick=APP_TICK
		)
	# app controller main loop
	app_controller.run()
	
if __name__ == '__main__':
    main()

#============================[ TODOs section ]=================================
""" 
TODO: 
replace prints for logging

TODO: 
if beacons controller grows up, it must have features like get_nearest_beacon
get_beacon_list, clear_beacons_list, set_order_type

TODO:
receive kwargs

TODO:
Ponerle el atributo last near beacon con property
"""
#============================[ End of file ]==================================