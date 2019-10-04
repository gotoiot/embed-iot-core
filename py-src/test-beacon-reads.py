import time
from beacontools import BeaconScanner, IBeaconFilter

TIME_TO_SCAN = 10
BEACON_UUID  = "ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee"

def main():

	def callback(bt_addr, rssi, packet, additional_info):
		print("[ MAC: {} | RSSI: {} ] - {}".format(bt_addr, rssi, packet))

	# scan for all iBeacon advertisements from beacons with the specified uuid
	scanner = BeaconScanner(callback, device_filter=IBeaconFilter(uuid = BEACON_UUID))
	# start scanning
	print ("Starting to scan beacons with UUID={} for {} seconds".format(BEACON_UUID, TIME_TO_SCAN))
	scanner.start()
	time.sleep(TIME_TO_SCAN)
	scanner.stop()
	print ("Scan beacons finished!")

if __name__ == "__main__":
	main()