import asyncio
import json
import pymavlink.mavutil as mavutil
import time
from flask import request

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    x = request.data.decode("utf-8")
    import pdb; pdb.set_trace()
    return x

    # return "Fuck shit"

if __name__ == "__main__":
    app.debug = True
    app.run()