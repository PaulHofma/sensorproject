import itertools
from flask import Flask, Response, redirect, request, url_for, render_template, current_app
from http import HTTPStatus

VERSION = "0.1.0"

def create_app(announcer):
    global VERSION
    
    app = Flask(__name__)
    app.config['ANNOUNCER'] = announcer

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
    
    return app

