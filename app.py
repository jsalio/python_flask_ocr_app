import time
from controller.RootApp import app_api
from controller.UploadApi import upload_api

import redis
from flask import Flask

app = Flask(__name__)
app.register_blueprint(app_api)
app.register_blueprint(upload_api)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times. Welcome to python Loser x \n'.format(count)