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
