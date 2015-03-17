#!/usr/bin/env python3.4

import asyncio
import json
import pymavlink.mavutil as mavutil
import time
import api

device = ":20000"
mavproxy_conn = mavutil.mavlink_connection(device)
heartbeat_message = mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = False)


from flask import Flask, render_template

app = Flask(__name__)

class EventSender(app.response_class):
    @asyncio.coroutine
    def __call__(self, environ, start_response):
        write = start_response('200 OK', [('content-type', 'text/event-stream')])
        write(b"data: welcome\n\n")
        while True:
            data = yield from asyncio.wait_for(location(),
                                               timeout=1.0)
            yield from postmessage(data,write)
            #data = yield from asyncio.wait_for(status(),
            #                                   timeout=1.0)
            #yield from postmessage(data,write)

    def __init__(self): pass
    __enter__ = None
    close = None
    call_on_close = None

@asyncio.coroutine
def postmessage(data,write):
        response = ('data: {0}\n\n'.format(data).encode('utf-8'))
        write(response)

@app.route('/async')
def async():
    return EventSender()

@app.route('/')
def root():
    return EventSender()

# Systems
@app.route('/uav/1/systems/reboot')
def reboot():
    return api.reboot()

@app.route('/uav/1/sytems/packet_loss')
def packet_loss():
    return mavproxy_conn.packet_loss()

@app.route('/uav/1/systems/time_since')
def time_since(mtype):
    '''Returns time difference in epoch time'''
    return mavproxy_conn.time_since(mtype)

@app.route('/uav/1/systems/set_servo')
def set_servo(channel, pwm):
    # Check pararmeters being passed along in this request
    mavproxy_conn.set_servo(channel, pwm)
    return 'Servo %s set to %s' % (channel, pwm)

@app.route('/uav/1/systems/set_relay')
def set_relay(relay_pin, state):
    '''Set relay pin n to state 0 or 1'''
    mavproxy_conn.set_relay(relay_pin)
    if (state):
        state = 'ON'
    else:
        state = 'OFF'
    return 'Relay pin %s set to %s' % (str(relay_pin), state)

@app.route('/uav/1/systems/calibrate_gyro')
def calibrate_gyro():
    mavproxy_conn.calibrate_imu()
    return 'GYRO CALIBRATED'

@app.route('/uav/1/systems/calibrate_level')
def calibrate_level():
    mavproxy_conn.calibrate_level()
    return 'LEVEL CALIBRATED'

@app.route('/uav/1/systems/calibrate_pressure')
def calubrate_pressure():
    mavproxy_conn.calibrate_pressure()
    return 'PRESSURE CALIBRATED'

# Modes
@app.route('/uav/1/modes/mode_mapping')
def mode_mapping():
    return mavproxy_conn.mode_mapping()

@app.route('/uav/1/modes/rtl')
def rtl():
    print(mavutil.mode_string_v10(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)))
    mavproxy_conn.set_mode('RTL')
    return 'RTL'

@app.route('/uav/1/modes/stabilize')
def stabilize():
    print(mavutil.mode_string_v10(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)))
    mavproxy_conn.set_mode('STABILIZE')
    return 'STABILIZE'

@app.route('/uav/1/modes/auto')
def auto():
    print(mavutil.mode_string_v10(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)))
    mavproxy_conn.set_mode('AUTO')
    return 'AUTO'

@app.route('/uav/1/modes/loiter')
def loiter():
    print(mavutil.mode_string_v10(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)))
    mavproxy_conn.set_mode('LOITER')
    return 'LOITER'

# Waypoints
@app.route('/uav/1/waypoints/send')
def waypoint():
    print(mavutil.mode_string_v10(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)))
    mavproxy_conn.send_waypoint(37.5720062256,-122.3333129883,67)
    return 'WAYPOINT'

@app.route('/uav/1/waypoints/clear')
def clear_waypoints():
    print(mavutil.mode_string_v10(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)))
    mavproxy_conn.waypoint_clear_all_send()
    return 'CLEAR'

@app.route('/uav/1/waypoints/current')
def current_waypoint():
    return mavproxy_conn.waypoint_current()


@app.route('/flask')
def flask():
    return render_template('some_flask_template.html')

@app.route('/hello')
def hello():
    return 'Hello'

@asyncio.coroutine
def location():
        location = mavproxy_conn.location()
        attitude = mavproxy_conn.attitude()
        waypoint = mavproxy_conn.waypoint_current()
        mode = mavproxy_conn.flightmode
        vehicletype = mavproxy_conn.vehicle_type
        bat = mavproxy_conn.battery()
        data = {'result':{
                        'location':{ 
                        'latitude':location.lat,
                        'longitude':location.lng, 
                        'altitude':location.alt, 
                        'heading':location.heading,
                        'airspeed':location.airspeed,
                        'groundspeed':location.groundspeed,
                        'climb':location.climb,
                        'throttle':location.throttle
                        },
                        'waypoints':{
                        'current':waypoint
                        },
                        'attitude':{
                        'pitch':attitude.pitch,
                        'roll':attitude.roll,
                        'yaw':attitude.yaw
                        },
                        'status':{
                        'mode':mode, 
                        'type':vehicletype,
                        },
                        'battery':{
                        'voltage':bat.voltage,
                        'current':bat.current,
                        'remaining':bat.remaining
                        }
                    }
                }
        data = json.dumps(data)
        return data

@asyncio.coroutine
def status():
        mode = mavproxy_conn.flightmode
        vehicletype = mavproxy_conn.vehicle_type
        bat = mavproxy_conn.battery()
        data = {'result':{ 
                    'status':{
                        'mode':mode, 
                        'type':vehicletype,
                        },
                        'battery':{
                        'voltage':bat.voltage,
                        'current':bat.current,
                        'remaining':bat.remaining
                        }
                    }
                }
        data = json.dumps(data)
        return data 

if __name__ == "__main__":

    app.debug = True

    import aiohttp.wsgi

    loop = asyncio.get_event_loop()
    f = loop.create_server(lambda: aiohttp.wsgi.WSGIServerHttpProtocol(app, debug=True, readpayload=False), "0.0.0.0", 5000)
    srv = loop.run_until_complete(f)
    socks = srv.sockets
    print("serving on", [x.getsockname() for x in socks])
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

