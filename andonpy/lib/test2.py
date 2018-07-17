#!/usr/bin/env python
# Siwanont Sittinam
# Test 2

from flask import Flask, request
import logging
import netifaces

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

# for interface in netifaces.interfaces():
    # ip = netifaces.ifaddresses(interface)
    # print(interface + " " + ip[2][0]['addr'])


@app.route("/")
def hello():
    return "Hello"

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == "__main__":
    app.run()
