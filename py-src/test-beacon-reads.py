import argparse
import time

from beacontools import BeaconScanner
from beacontools import IBeaconFilter

DEFAULT_TIME_TO_SCAN = 10
DEFAULT_BEACON_UUID  = "ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee"

def main():
	# callback to show beacons read
	def callback(bt_addr, rssi, packet, additional_info):
		print("[ MAC: {} | RSSI: {} ] - {}".format(bt_addr, rssi, packet))
	# intance the parser
	parser = argparse.ArgumentParser()
	parser.add_argument('--uuid', action='store', dest='uuid',
						help='iBeacon UUID. Def: {}'.format(DEFAULT_BEACON_UUID))
	parser.add_argument('--time', action='store', dest='scan_time',
						help='Scan time. Def: {}'.format(DEFAULT_TIME_TO_SCAN))
	# get result of parse arguments in 'r'
	res = parser.parse_args()
	uuid = res.uuid if res.uuid is not None else DEFAULT_BEACON_UUID
	scan_time = res.scan_time if res.scan_time is not None else DEFAULT_TIME_TO_SCAN
	# scan for all iBeacon advertisements from beacons with the specified uuid
	scanner = BeaconScanner(callback, device_filter=IBeaconFilter(uuid = uuid))
	# start scanning
	print ("Starting to scan beacons with UUID={} for {} seconds".format(uuid, scan_time))
	scanner.start()
	time.sleep(scan_time)
	scanner.stop()
	print ("Scan beacons finished!")

if __name__ == "__main__":
	main()