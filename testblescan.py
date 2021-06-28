# test BLE Scanning software

from beaconAd import beaconAd
import blescan
import sys

import bluetooth._bluetooth as bluez

dev_id = 2
try:
    sock1 = bluez.hci_open_dev(1)
    sock2 = bluez.hci_open_dev(2)
    print("ble thread started")

except:
    print("error accessing bluetooth device...")
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock1)
blescan.hci_enable_le_scan(sock1)
blescan.hci_le_set_scan_parameters(sock2)
blescan.hci_enable_le_scan(sock2)

while True:
    returnedList1 = blescan.parse_events(sock1, 10)
    returnedList2 = blescan.parse_events(sock2, 10)
    print("1----------1")
    for beacon in returnedList1:
        ad = beaconAd.from_str(beacon)
        if (ad.major == 3839):
            print(beacon)
    print("2----------2")
    for beacon in returnedList2:
        ad = beaconAd.from_str(beacon)
        if (ad.major == 3839):
            print(beacon)

