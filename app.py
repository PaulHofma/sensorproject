import itertools
import time
from flask import Flask, Response, redirect, request, url_for, render_template
from http import HTTPStatus
from sensors import getReadout

app = Flask(__name__)
VERSION = "0.1.0"

FAIL_COUNTER = []
TEMP = []
HMD = []
TIME = []

@app.route("/health")
def health():
    return ("", HTTPStatus.NO_CONTENT)

@app.route("/version")
def version():
    return VERSION

@app.route("/")
def index():
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            global TEMP
            global HMD
            global TIME
            global FAIL_COUNTER
            for _ in enumerate(itertools.count()):
                result = getReadout()
                if(result != ""):
                    data_update(TEMP, result['tmp'])
                    data_update(HMD, result['hmd'])
                    data_update(TIME, time.time())
                    yield 'data: {"data": "%s (%s)", "errors": %d, "tmp": %s, "hmd":%s, "timestamp":%s}\n\n' % (
                        result['printable'], time.strftime("%y%m%d %H:%M:%S", time.localtime()), len(FAIL_COUNTER), TEMP, HMD, TIME
                        )
                else:
                    FAIL_COUNTER.append(time.time())
                    yield 'data: {"errors": %d}\n\n' % len(FAIL_COUNTER)
                FAIL_COUNTER = [x for x in FAIL_COUNTER if (x+3600) > time.time()]
                time.sleep(5.0)
        return Response(events(), content_type='text/event-stream')
    return render_template('index.html', version=VERSION)


def data_update(data_in, val):
    if(len(data_in) <=10000):
        data_in = data_in.append(val)
    else:
        data_in = data_in.append(val)[1:]
        
