import itertools
from flask import Flask, Response, redirect, request, url_for, render_template, current_app, jsonify
from http import HTTPStatus
import asyncio

VERSION = "0.1.0"

def create_app(announcer, plugController):
    global VERSION
    
    app = Flask(__name__)
    app.config['ANNOUNCER'] = announcer
    app.config['CONTROLLER'] = plugController

    @app.route("/health")
    def health():
        return ("server ok", HTTPStatus.OK)

    @app.route("/version")
    def version():
        return VERSION

    @app.route("/")
    def index():
        print('getting page')
        globalAnnouncer = current_app.config['ANNOUNCER']
        if request.headers.get('accept') == 'text/event-stream':
            def stream():
                live = True
                messageQueue = globalAnnouncer.listen()
                if(app.debug):
                    print('listening: ' + str(globalAnnouncer))
                    print(globalAnnouncer.listeners)
                while live:
                    try:
                        msg = messageQueue.get(timeout=11)
                        if(app.debug):
                            print('got one!')
                        yield msg
                    except Exception as error:
                        live = False
                        yield ""
            return Response(stream(), content_type='text/event-stream')
        return render_template('index.html', version=VERSION)
    
    
    @app.route("/toggle", methods=["POST"])
    def manual_toggle():
        print("toggle!")
        pc = current_app.config['CONTROLLER']
        
        request_data = request.get_json()
        plug_number = request_data.get('plug_number')
        
        if plug_number is None:
            return jsonify({"error": "Missing 'plug_number' in the request body"}), 400
        
        res = asyncio.run(pc.toggle(plug_number))
        response_data = {"status": res}
        return jsonify(response_data)
    
    @app.route("/get-state", methods=["POST"])
    def get_state():
        print("ison!")
        pc = current_app.config['CONTROLLER']
        
        request_data = request.get_json()
        plug_number = request_data.get('plug_number')
        
        if plug_number is None:
            return jsonify({"error": "Missing 'plug_number' in the request body"}), 400
        
        res = asyncio.run(pc.is_on(plug_number))
        response_data = {"status": res}
        return jsonify(response_data)
    
    
    return app

