#!/usr/bin/env python
# Siwanont Sittinam
# Recognition

from flask import Flask, render_template, request, Response, redirect, url_for
import logging as logging

import sys
import os
import cv2 as cv
from picamera import PiCamera
from picamera.array import PiRGBArray
from lib.utility import Utility

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

util = Utility()
user_all = util.User()
train_path = util.TRAINPath()

recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read(train_path[0])

# Initial face_cascade lib path
face_cascade = cv.CascadeClassifier(util.HAARPath())

name = "unknown"

@app.route('/')
def index():
    return render_template('index.html')


def stream():
    global name

    with PiCamera(resolution=(1280, 720), framerate=90) as camera:
        print("[Initial] Camera is active...")
        print("[Initial] Please look at the camera and wait a minute...")

        camera.rotation = 180
        camera.brightness = 60
        camera.contrast = 5
        stream = PiRGBArray(camera)

        for frame in camera.capture_continuous(stream, format="bgr", use_video_port=True):
            image = frame.array
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                # Check if confidence is less them 100 ==> "0" is perfect match
                name = "unknown"
                if (confidence < 100):
                    name = user_all[id][1]
                cv.putText(image, name, (x+5, y-5), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            cv.imwrite("img.jpg", image)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open('img.jpg', 'rb').read() + b'\r\n')

            # if not name is "unknown":
                # util.updateUser()
                # return name

            stream.truncate()
            stream.seek(0)

@app.route('/frame')
def frame():
    return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':
    print('[Initial] Recognition with camera')
    for ip in util.getIP():
        print("[Initial]  * Running on http://"+ ip[1] + ":5000/ for interfaces " + ip[0])
    print("[Initial] Please open the following link.")
    app.run(host='0.0.0.0', threaded=True)
