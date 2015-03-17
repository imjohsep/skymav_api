#!flask/bin/python

from flask import Flask, jsonify, request
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from mav import MavRequest as Conn

app = Flask(__name__, static_url_path="")
api = Api(app)


class UsersList(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", type=str)
        super(UsersList, self).__init__()

    def get(self):
        return {"content": "All users"}, 200

    def post(self):
        message = request.json['email']
        return {"content": message}, 201

class Users(Resource):
    def get(self, id):
        return {"content": "Get specific user"}

    def put(self, id):
        return {"content": ""}

    def delete(self, id):
        return {"content": "User has been deleted"}

class UavsList(Resource):
    def get(self, id):
        return {"content": "Get Uav"}

    def post(self, id):
        return {"content": "Create new uav"}

class Uavs(Resource):
    def get(self, id, uav_id):
        return {"content": "Return single Uav"}

    def delete(self, id, uav_id):
        return {"content": "Delete a uav"}

class WaypointsList(Resource):
    def get(self, id, uav_id):
        return {"content": "Get a uav"}

    def post(self, id, uav_id):
        return {"content": "Post a mission of waypoints or add a single waypoint"}

class Waypoints(Resource):
    def get(self, id, uav_id, index):
        return {"content": "Get a single Waypoint"}

    def put(self, id, uav_id, index):
        return {"content": "Update waypoint at indexed position"}

    def delete(self, id, uav_id, index):
        return {"content": "Delete a single Waypoint"}

class Battery(Resource):
    def get (self, id, uav_id):
        return {"content": "Return battery level"}

class Reboot(Resource):
    def get(self, id, uav_id):
        return {"content": "Reboot system"}

class PacketLoss(Resource):
    def get(self, id, uav_id):
        return {"content": "Return packet loss amount"}

class TimeSince(Resource):
    def get(self, id, uav_id, mtype):
        return {"content": "Return time since mytype"}

class Servos(Resource):
    def post(self, id, uav_id, pwm):
        return {"content": "Set servo to pwm"}

class Mode(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('mode', type = str, location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('done', type = bool, location = 'json')
        super(TaskAPI, self).__init__()

    """Set Mode for a given UAV"""
    def post(self, id, uav_id, mode):
        return {"content": "Mode has been set"}

class ModeList(Resource):
    def __init__(self):
        self.conn = Conn()

    """ Get the current Mode of a given UAV """
    def get(self, id, uav_id):
        x = self.conn.getMode()
        return {"content": "The mode for UAV %s is %s" % (uav_id, self.conn.getMode())}



api.add_resource(UsersList, "/v2/users", endpoint="users")
api.add_resource(Users, "/v2/users/<int:id>", endpoint="user")
api.add_resource(UavsList, "/v2/users/<int:id>/uavs", endpoint="uavs")
api.add_resource(Uavs, "/v2/users/<int:id>/uavs/<int:uav_id>", endpoint="uav")
api.add_resource(WaypointsList, "/v2/users/<int:id>/uavs/<int:uav_id>/waypoints", endpoint="waypoints")
api.add_resource(Waypoints, "/v2/users/<int:id>/uavs/<int:uav_id>/waypoints/<int:index>", endpoint="waypoint")
api.add_resource(Battery, "/v2/users/<int:id>/uavs/<int:uav_id>/systems/battery", endpoint="battery")
api.add_resource(Reboot, "/v2/users/<int:id>/uavs/<int:uav_id>/systems/reboot", endpoint="reboot")
api.add_resource(PacketLoss, "/v2/users/<int:id>/uavs/<int:uav_id>/systems/packetloss", endpoint="packet_loss")
api.add_resource(TimeSince, "/v2/users/<int:id>/uavs/<int:uav_id>/systems/timesince/<string:mtype>", endpoint="time_since")
api.add_resource(Servos, "/v2/users/<int:id>/uavs/<int:uav_id>/systems/servos", endpoint="servos")
api.add_resource(ModeList, "/v2/users/<int:id>/uavs/<int:uav_id>/modes", endpoint="modes")
api.add_resource(Mode, "/v2/users/<int:id>/uavs/<int:uav_id>/modes/<string:mode>", endpoint="mode")


if __name__ == "__main__":
    app.run(debug=True)