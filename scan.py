#!/usr/bin/env python3

import blescan
import sys
import multiprocessing

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

    def distance(self):
        ratio = self.rssi / self.tx_power
        if ratio < 1.0:
            return ratio ** 10
        else:
            return 0.89976 * (ratio ** 7.7095) + 0.111

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
            if ad.major == 3838:
                print(ad.uuid, ad.major, ad.minor, ad.tx_power, ad.rssi)
                print("tx_power={}, rssi={}, distance={}".format(ad.tx_power, ad.rssi, ad.distance()))

def sock_setup(dev_id):
    try:
        sock = bluez.hci_open_dev(dev_id)
        print("ble thread started")

    except:
        print("error accessing bluetooth device...")
        sys.exit(1)

    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
    return sock

def scan_once(sock, major, idx=0, return_array=None):
    returnedList = blescan.parse_events(sock, 100)
    print("----------")
    ad_count = 0
    total_dist = 0
    for beacon in returnedList:
        ad = beaconAd.from_str(beacon)
        if ad.major == major:
            ad_count += 1
            total_dist += ad.distance()

    if ad_count > 0:
        dist = total_dist / ad_count
    else:
        dist = float('inf')
    if return_array:
        return_array[idx] = dist
    return dist

if __name__ == "__main__":
    major = 3838
    sockets = []
    num_sensors = 1
    rets = multiprocessing.Array("d", [0.0]*num_sensors, lock=True)

    for i in range(num_sensors):
        sock = sock_setup(i)
        sockets.append(sock)

    while True:
        processes = []

        for i in range(num_sensors):
            p = multiprocessing.Process(target=scan_once, args=[sock, major, rets])
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        print(rets[:])
