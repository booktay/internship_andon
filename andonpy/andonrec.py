#!/usr/bin/env python
# Siwanont Sittinam
# Main

from flask import Flask, jsonify, render_template, request, Response, redirect, url_for

# Import management linux system module
import sys
import os
# Import image processing module
import cv2 as cv
# Import delay module
from time import sleep
# Import PiCamera Module
from picamera import PiCamera
from picamera.array import PiRGBArray
from lib.utility import Utility
# from .lib.database import DatabaseConnection

app = Flask(__name__)

util = Utility()

# recognizer = cv.face.LBPHFaceRecognizer_create()
# recognizer.read(util.TRAINPath())

# Initial face_cascade lib path
face_cascade = cv.CascadeClassifier(util.HAARPath())

#Config font
font = cv.FONT_HERSHEY_SIMPLEX


name = "unknown"


@app.route('/')
def index():
    return render_template('index.html')


def stream():
    with PiCamera(resolution=(1280, 720), framerate=40) as camera:
        print("[Initial] Camera is active...")
        print("[Initial] Please look at the camera and wait a minute...")

        camera.rotation = 180
        camera.brightness = 60
        camera.contrast = -5
        stream = PiRGBArray(camera)

        count = 0
        check_user = util.haveUser("books")
        for frame in camera.capture_continuous(stream, format="bgr", use_video_port=True):
            image = frame.array
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                count += 1
                cv.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                if not check_user[0] is "0" and count < 100:
                    filename = check_user[0] + '.' + check_user[1] + "." + str(count) + ".jpg"
                    cv.imwrite(os.path.join(check_user[2], filename), image[y:y+h, x:x+w])
                if count == 15:
                    camera.close()

            cv.imwrite("img.jpg", image)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open('img.jpg', 'rb').read() + b'\r\n')

            stream.truncate()
            stream.seek(0)

@app.route('/show_rec')
def show_rec():
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
    app.run(host='0.0.0.0', threaded=True)
