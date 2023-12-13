import itertools
import time
from flask import Flask, Response, redirect, request, url_for, render_template
from http import HTTPStatus
from sensors import getReadout
from main import MessageAnnouncer, main_process
import threading

app = Flask(__name__)
VERSION = "0.1.0"
print(f"application master starting up, should run only once...") 

FAIL_COUNTER = []
TEMP = []
HMD = []
TIME = []
ANNOUNCER = MessageAnnouncer()

def background():
    print('start background process...')
    main_process(TEMP, HMD, TIME, FAIL_COUNTER, ANNOUNCER)
    
mp = threading.Thread(name='bg', target=background)
mp.start()

@app.route("/health")
def health():
    return ("", HTTPStatus.NO_CONTENT)

@app.route("/version")
def version():
    return VERSION    

@app.route("/")
def index():
    print('hi?')
    global ANNOUNCER
    if request.headers.get('accept') == 'text/event-stream':
        def stream():
            messages = ANNOUNCER.listen()
            while True:
                msg = messages.get()
                yield msg
                
        return Response(stream(), content_type='text/event-stream')
    return render_template('index.html', version=VERSION)

if __name__ == "__main__":
    print('arg')
    app.run()

