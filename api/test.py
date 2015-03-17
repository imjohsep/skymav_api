import pymavlink.mavutil as mavutil
import time

device = ":20000"
mavproxy_conn = mavutil.mavlink_connection(device)
heartbeat_message = mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)

#while True:
#	print(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True))
#	print(mavproxy_conn.location())
#	print(mavutil.mode_string_v10(heartbeat_message))

print(mavutil.mode_string_v10(heartbeat_message))
mavproxy_conn.set_mode_auto()
print(mavutil.mode_string_v10(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)))
mavproxy_conn.set_mode('RTL')
print(mavutil.mode_string_v10(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)))


#def device():
#	return device
#def connection():
#	return mavproxy_conn
