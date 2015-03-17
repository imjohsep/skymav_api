import pymavlink.mavutil as mavutil

class MavRequest:
    device = ''

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