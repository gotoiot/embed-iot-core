import subprocess
from beacontools import BeaconScanner
from beacontools import IBeaconFilter

APP_PERIODIC_TIME   = 1 
BEACONS_SCAN_TIME   = 2	
BEACONS_UUID        = "b9407f30-f5f8-466e-aff9-25556b57fe6d"
CMS_IP_ADDRESS      = "192.168.0.12"
CMS_PORT            = 9090

_beacons_list = []

class Beacon:
	def __init__(self, address, rssi, packet):
		self.address = address
		self.rssi = rssi
		self.packet = packet

def beacons_is_in_list(beacon):
	global _beacons_list
	is_item_in_list = False
	for item_list in _beacons_list:
		if item_list.address == beacon.address:
			is_item_in_list = True
	return is_item_in_list

def beacons_callback(bt_addr, rssi, packet, additional_info):
	global _beacons_list
	beacon = Beacon(bt_addr, rssi, packet)
	if (beacons_is_in_list(beacon) == False):
		_beacons_list.append(beacon)

def beacons_scan():
	global _beacons_list
    _beacons_list[:] = []
	scanner = BeaconScanner(
        beacons_callback, device_filter = IBeaconFilter(BEACONS_UUID))
	
	scanner.start()
	time.sleep(BEACONS_SCAN_TIME)
	scanner.stop()
	
	if len(_beacons_list) > 1:
		_beacons_list = sorted(
            _beacons_list, key = lambda beacon_aux: beacon_aux.rssi, reverse = True)
	
	for beacon in _beacons_list:
		print ("Beacon Address = %s, Rssi = %d" % (beacon.address, beacon.rssi))
		
def web_update(beacon_id):
    url = "http://{}:{}/beacons/{}".format(CMS_IP_ADDRESS, str(CMS_PORT), beacon_id)
    print ("Invoking URL: " + url)
    # p = subprocess.Popen(["chromium-browser", '--kiosk', '--incognito', web_url])
    # p = subprocess.Popen(["iceweasel", url])

def main():
	while (1):	
        beacons_scan()
        web_update(_beacons_list[0])
		time.sleep(APP_PERIODIC_TIME)
	
if __name__ == '__main__':
    main()

#============================[ End of file ]==================================

def TestBeacons():
	_beacons_last_address = ""
	_beacons_scan_count = 0
	while (1):
		_beacons_scan_count = _beacons_scan_count + 1
		if _beacons_scan_count >= 1:
			_beacons_scan_count = 0
			beacons_scan()	
			if len(_beacons_list) > 0:
				print "Beacon elegido, Addr= %s" % _beacons_list[0].address
				if(_beacons_last_address != _beacons_list[0].address):
					_beacons_last_address = _beacons_list[0].address
		
		time.sleep(1)			
	return