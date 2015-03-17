#!/usr/bin/env python3.4
#/area52/api/app.py

import asyncio
import json
import pymavlink.mavutil as mavutil
import time
from flask import request

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

@app.route('/event')
def root():
    return EventSender()

@app.route('/uav/<int: uav_id>/mode/rtl')
def rtl():
    print(mavutil.mode_string_v10(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)))
    mavproxy_conn.set_mode('RTL')
    return 'RTL'

@app.route('/uav/<int: uav_id>/mode/stabilize')
def stabilize():
    print(mavutil.mode_string_v10(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)))
    mavproxy_conn.set_mode('STABILIZE')
    return 'STABILIZE'

@app.route('/uav/<int: uav_id>/mode/auto')
def auto():
    print(mavutil.mode_string_v10(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)))
    mavproxy_conn.set_mode('AUTO')
    return 'AUTO'

@app.route('/uav/<int: uav_id>/mode/loiter')
def loiter():
    print(mavutil.mode_string_v10(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)))
    mavproxy_conn.set_mode('LOITER')
    return 'LOITER'

@app.route('/uav/<int: uav_id>/system/reboot')
def reboot():
    print(mavutil.mode_string_v10(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)))
    mavproxy_conn.reboot_autopilot()
    return 'REBOOT'

@app.route('/uav/<int: uav_id>/waypoints/current')
def current_waypoint():
    return mavproxy_conn.current_waypoint()

@app.route('/uav/<int: uav_id>/waypoints/send')
def waypoint():
    print(mavutil.mode_string_v10(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)))
    mavproxy_conn.send_waypoint(37.5720062256,-122.3333129883,67)
    return 'WAYPOINT'

@app.route('/uav/<int: uav_id>/waypoints/clear')
def clear_waypoints():
    print(mavutil.mode_string_v10(mavproxy_conn.recv_match (type = 'HEARTBEAT', blocking = True)))
    mavproxy_conn.waypoint_clear_all_send()
    return 'CLEAR'

@app.route('/flask')
def flask():
    return render_template('some_flask_template.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    return request.data
    # return "Fuck shit"

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