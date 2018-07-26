from flask import Flask, render_template, request, Response, redirect, url_for
import logging as logging

from picamera import PiCamera
from picamera.array import PiRGBArray

import sys as sys
import os as os
import cv2 as cv

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

from .utility import Utility
util = Utility()

face_cascade = cv.CascadeClassifier(util.HAARPath())

verif = "False"

class CreateDataset():

    def __init__(self, username):
        self.name = username
        global name
        name = username

    def run(self):
        util.getIP()
        app.run(host='0.0.0.0', port=5001, threaded=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getshutdown')
def getshutdown():
    global verif
    return verif

def createDataset():
    global name
    global verif

    USER = name
    check_user = util.haveUser(USER)
    if check_user[0] is "0":
        USER_PATH = str(util.numUser()) + "." + USER
        PATH = os.path.join(util.IMGROOTPath(),USER_PATH)
        os.mkdir(PATH)
        print("[Initial] Create " + USER + " dataset")
    else:
        print("[Initial] Found " + check_user[1] + " dataset")
        print("[Initial] Recreate " + check_user[1] + " dataset")

    check_user = util.haveUser(USER)
    with PiCamera(resolution=(1280, 720), framerate=40) as camera:
        print("[Initial] Camera is active...")
        print("[Initial] Please look at the camera and wait a minute...")

        # camera.rotation = 180
        camera.brightness = 55
        camera.contrast = 5
        stream = PiRGBArray(camera)

        count = 0
        verif = "False"

        for frame in camera.capture_continuous(stream, format="bgr", use_video_port=True):
            if count >= 100:
                print("[Successful] create 100 images")
                verif = "True"
                break

            image = frame.array
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                count += 1
                cv.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                filename = check_user[0] + '.' + check_user[1] + "." + str(count) + ".jpg"
                cv.imwrite(os.path.join(check_user[2], filename), image[y:y+h, x:x+w])
                print("[Save] " + filename)

            cv.imwrite("img.jpg", image)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open('img.jpg', 'rb').read() + b'\r\n')

            stream.truncate()
            stream.seek(0)


@app.route('/frame')
def frame():
    return Response(createDataset(), mimetype='multipart/x-mixed-replace; boundary=frame')


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return "[No service] Server is closed"


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
