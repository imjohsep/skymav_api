import json
import asyncio
import pymavlink.mavutil as mavutil
from base import Base
from api import Api
from flask import Flask, request, render_template, jsonify, make_response, abort

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_content(error):
	return make_response(jsonify({'error': 'Bad content'}), 400)

@app.route('/post', methods=['GET', 'POST'])
def post():
	req = Base(request)
	message = req.getMessage()
	return message['fuck']

@app.route('/', methods=['GET', 'POST'])
def index():	
	return "hello, world"


@app.route('/waypoints', methods=['POST'])
def waypoint():
	"""
		----ERROR----
		<class 'struct.error'>
		required argument is not a float
		
		<class 'OSError'>
		[Errno 48] Address already in use
		-------------
	"""
	req = Api(request)
	waypoint = req.getWaypoint()
	try:
		device = ":20000"
		mavproxy_conn = mavutil.mavlink_connection(device)
		mavproxy_conn.send_waypoint(float(waypoint.latitude), 
									float(waypoint.longitude), 
									float(waypoint.altitude))
		success = True
	except Exception as e:
		print("----ERROR----")
		print(type(e))
		print(e)
		print("-------------")
	finally:
		data = {'success': True,
				'latitude': float(waypoint.latitude),
				'longitude': float(waypoint.longitude),
				'altitude': float(waypoint.altitude)}
		
		data = jsonify(data)
		return data

@app.route('/mission/begin')
def begin():
	device = ":20000"
	mavproxy_conn = mavutil.mavlink_connection(device)
	mavproxy_conn.waypoint_request_list_send() # Get waypoint list
	if not mavproxy_conn.motors_armed: # If drone isn't armed
		mavproxy_conn.arducopter_arm() # Arm drone
		# mavproxy_conn.motors_armed_wait() # Wait for motors to be armed
	if mavproxy_conn.motors_armed
		mavproxy_conn.set_mode('LOITER') # Prepare for mission
		mavproxy_conn.set_mode('AUTO') # Begin mission

if __name__ == "__main__":

    app.run(debug=True)