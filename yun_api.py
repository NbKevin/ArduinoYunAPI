from flask import Flask
from flask.ext.restful import Api

from api import YunRealtimeReadingsAPI, YunRealtimeHeartRateAPI
from config_ import YUN_API_CONFIG
from utilities import set_up_flask
from yun.heart_rate_adapter import _HeartRateThread

# flask app
app = Flask(__name__)
set_up_flask(app)

# restful api
api = Api(app)
api.add_resource(YunRealtimeReadingsAPI, '/api/realtime/')
api.add_resource(YunRealtimeHeartRateAPI, '/api/heartrate/')

# start the background thread
_HeartRateThread().start()

if __name__ == '__main__':
    app.run(host=YUN_API_CONFIG.flask_host, port=YUN_API_CONFIG.flask_port)
