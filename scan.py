#!/usr/bin/env python3

import blescan
import sys

import bluetooth._bluetooth as bluez

class beaconAd:
    def __init__(self, mac, uuid, major, minor, tx_power, rssi) -> None:
        self.mac = mac
        self.uuid = uuid
        self.major = major
        self.minor = minor
        self.tx_power = tx_power
        self.rssi = rssi
    
    @classmethod
    def from_str(cls, adstring):
        adlist = adstring.split(",")
        mac = adlist[0]
        uuid = adlist[1]
        major = int(adlist[2])
        minor = int(adlist[3])
        tx_power = int(adlist[4])
        rssi = int(adlist[5])
        return cls(mac, uuid, major, minor, tx_power, rssi)

def scan_at(dev_id):
    try:
        sock = bluez.hci_open_dev(dev_id)
        print("ble thread started")

    except:
        print("error accessing bluetooth device...")
        sys.exit(1)

    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)

    while True:
        returnedList = blescan.parse_events(sock, 100)
        print("----------")
        for beacon in returnedList:
            ad = beaconAd.from_str(beacon)
            if ad.major == 3939:
                print(ad.uuid, ad.major, ad.minor, ad.tx_power, ad.rssi)

if __name__ == "__main__":
    scan_at(1)