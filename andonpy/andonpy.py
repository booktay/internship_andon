#!/usr/bin/env python
# Siwanont Sittinam
# Main

from flask import Flask, jsonify, render_template, request, Response
# from lib.face_recognition import FaceRecognition
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
from lib.util import Utility
from lib.database import DatabaseConnection

app = Flask(__name__)

util = Utility()

recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read(util.trainPath())

# Initial face_cascade lib path
face_cascade = cv.CascadeClassifier(util.HAARpath())

#Config font
font = cv.FONT_HERSHEY_SIMPLEX

# Initial camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
rawCapture = PiRGBArray(camera, size=(640, 480))

name = "unknown"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_name')
def getName():
    # DatabaseConnection().updateStatusUser(name)
    return name

def stream():
    if camera:
        sleep(0.5)  # warmup
        print("[Initial] Camera is active...")

        id = 0
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            # flip image
            image = cv.flip(image, -1)
            # converse color to gray
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            # find face by HAARCascade algorithm
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            # draw face in image
            for (x, y, w, h) in faces:
                cv.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                # Check if confidence is less them 100 ==> "0" is perfect match
                global name
                if (confidence < 100): name = util.findUname(id)
                cv.putText(image, name, (x+5, y-5), font, 1, (255, 255, 0), 2)

            cv.imwrite("img.jpg", image)

            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + open('img.jpg', 'rb').read() + b'\r\n')

            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)


@app.route('/show_rec')
def show_rec():
    return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
