#! /usr/bin/bash
gunicorn wsgi --bind 0.0.0.0:8000 --threads 4 --preload --worker-class=gevent --workers=2
