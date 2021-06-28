#!/usr/bin/env python3

import blescan
import sys
from beaconAd import beaconAd
import bluetooth._bluetooth as bluez


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
    returnedList = blescan.parse_events(sock, 5)
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
    major = 3839
    sockets = []
    sensor_list = [1, 2]
    rets = [0.0] * len(sensor_list)

    for i in sensor_list:
        sock = sock_setup(i)
        sockets.append(sock)

    while True:
        for i in range(len(sensor_list)):
            rets[i] = scan_once(sockets[i], major)
        print("----------")
        print(', '.join('{:.3f}'.format(f) for f in rets))
