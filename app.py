import itertools
import time
from flask import Flask, Response, redirect, request, url_for, render_template
from http import HTTPStatus
from sensors import getReadout

app = Flask(__name__)
VERSION = "0.1.0"


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
            FAIL_COUNTER = []
            for _ in enumerate(itertools.count()):
                x = getReadout()
                if(x != ""):
                    yield 'data: {"data": "%s (%s)", "errors": %d}\n\n' % (getReadout(), time.strftime("%y%m%d %H:%M:%S", time.localtime()), len(FAIL_COUNTER))
                else:
                    FAIL_COUNTER.append(time.time())
                    yield 'data: {"errors": %d}\n\n' % len(FAIL_COUNTER)
                FAIL_COUNTER = [x for x in FAIL_COUNTER if (x+3600) > time.time()]
                time.sleep(5.0)
        return Response(events(), content_type='text/event-stream')
    return render_template('index.html', version=VERSION)