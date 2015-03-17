from flask import Flask
import json

app = Flask(__name__)

@app.route("/uav/1/trackingstations")
def available_servers():
		data = {'result':[
						{
						'url':'http://area52.skymav.com',
						'port':'21000'
						},
						{
						'url':'http://area51.skymav.com',
						'port':'21000'
						}
					]
				}
		data = json.dumps(data)
		return data

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)