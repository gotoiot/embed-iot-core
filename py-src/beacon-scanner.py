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
		print("BeaconsController ('uuid_filter': '{}', 'scan_tick': '{}')".format(
			uuid_filter, scan_tick))
		self._beacons_list = []
		self._uuid_filter = uuid_filter
		self._scan_tick = scan_tick
		self.__nearest_beacon = Beacon("", "", 0, 0, 0, 0)

	def _is_beacon_in_list(self, beacon):
		for beacon_item in self._beacons_list:
			if beacon_item.major == beacon.major and beacon_item.minor == beacon.minor:
				return = True
		return False

	def _order_beacons_list(self, oderType=None):
		self._beacons_list = sorted(
			self._beacons_list, 
			key = lambda beacon : beacon.rssi, 
			reverse = True
			)

	def update(self):

		def _scans_callback(bt_addr, rssi, packet, additional_info):
			beacon = Beacon(bt_addr, packet.uuid, packet.major, packet.minor, packet.tx_power, rssi)
			if not self._is_beacon_in_list(beacon):
				self._beacons_list.append(beacon)

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
			self.__nearest_beacon = self._beacons_list[0]
			print ("Nearest beacon: {}".format(self.__nearest_beacon))
		else:
			self.__nearest_beacon = None
			print("No beacons found in this scan")
		
		return self.__nearest_beacon

	def get_nearest_beacon_fake(self):
		import random

		self._beacons_list = []
		self._beacons_list.append(Beacon("11:11:11", BEACONS_FILTER, 0, 1, -50, random.randint(1, 100) * -1))
		self._beacons_list.append(Beacon("22:22:22", BEACONS_FILTER, 0, 2, -50, random.randint(1, 100) * -1))
		self._beacons_list.append(Beacon("33:33:33", BEACONS_FILTER, 0, 3, -50, random.randint(1, 100) * -1))

		if len(self._beacons_list) >= 1:
			self._order_beacons_list()
			self.__nearest_beacon = self._beacons_list[0]
			print ("Nearest beacon: {}".format(self.__nearest_beacon))
		else:
			self.__nearest_beacon = None
			print("No beacons found in this scan")

		return self.__nearest_beacon

	@property
	def nearest_beacon(self):
		return self.__nearest_beacon


class WebController:

	def __init__(self, cms_ip=CMS_IP, cms_port=CMS_PORT, cms_resource=CMS_RESOURCE):
		print("WebController ('cms_ip':'{}', 'cms_port': '{}', 'cms_resource': '{}')".format(cms_ip, cms_port, cms_resource))
		self.cms_ip = cms_ip
		self.cms_port = cms_port
		self.cms_resource = cms_resource

	def update_content(self, arguments):
		url = "http://{}:{}/{}?{}".format(self.cms_ip, self.cms_port, 
										  self.cms_resource, arguments)
		print ("Invoking URL: {}".format(url))
		process = subprocess.Popen(["iceweasel", url])
	
	def update_content_fake(self, arguments):
		url = "http://{}:{}/{}?{}".format(self.cms_ip, str(self.cms_port), 
											self.cms_resource, arguments)
		print ("Invoking URL: " + url)


class AppController:

	def __init__(self, beacons_controller=None, web_controller=None, app_tick=APP_TICK):
		self.app_tick = app_tick
		self.beacons_controller = beacons_controller
		self.web_controller = web_controller
		self.nearest_beacon = Beacon("", "", 0, 0, 0, 0)

	def _is_beacon_change(self, beacon):
		is_beacon_change = False
		if isinstance(beacon, Beacon) and (beacon.major != self.nearest_beacon.major or beacon.minor != self.nearest_beacon.minor):
			print("New nearest beacon: {}".format(beacon))
			is_beacon_change = True
		return is_beacon_change

	def _format_http_arguments(self, beacon):
		http_arguments = "uuid={}&major={}&minor={}".format(
			beacon.uuid, beacon.major, beacon.minor)
		return http_arguments

	def run(self):
		while (1):
			self.beacons_controller.update()
			if self._is_beacon_change(self.beacons_controller.nearest_beacon):
				self.nearest_beacon = self.beacons_controller.nearest_beacon
				http_arguments = self._format_http_arguments(self.nearest_beacon)
				self.web_controller.update_content_fake(http_arguments)
			time.sleep(self.app_tick)

# ======= [Main function] =====================================================

def main ():
	print ("Welcome to Beacons Scanner for Raspberry Pi - Powered by Agustin Bassi")

	beacons_controller = BeaconsController(
		uuid_filter=BEACONS_FILTER, 
		scan_tick=SCAN_TICK
		)	

	web_controller = WebController(
		cms_ip=CMS_IP, 
		cms_port=CMS_PORT, 
		cms_resource=CMS_RESOURCE
		)
	
	app_controller = AppController(
		beacons_controller=beacons_controller, 
		web_controller=web_controller,
		app_tick=APP_TICK
		)

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