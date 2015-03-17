import pymavlink.mavutil as mavutil

class MavRequest:
    device = ''
    modes = {'rtl': 'RTL', 'loiter': 'LOITER', 'auto': 'AUTO', 'stabalize': 'STABALIZE'}

    def __init__(self):
        self.device = ":20000"
        self.conn = mavutil.mavlink_connection(self.device)
    
    def getDevice(self):
        return self.device

    def setDevice(self, device):
        self.device = device
        return self.device

    def newConnection(self, device):
        self.conn = mavutil.mavlink_connection(device)
        return self.conn

    def getMode(self):
        mode = self.conn.flightmode
        if (mode == 'UNKNOWN'):
            return "Unknown"
        else:
            return mode

    def setMode(self, mode):
        if mode in self.modes:
            self.conn.set_mode(self.modes[mode])
            return self.modes[mode]

    def getBattery(self):
        battery = self.conn.battery()
        return battery
