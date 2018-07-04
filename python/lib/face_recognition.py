# ===============================
# ====       Python 3.7      ====
# ====   Siwanont Sittinam   ====
# ==== Andon PiCamera Module ====
# ====   Face Recognition    ====
# ===============================

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

class FaceRecognition:

    def __init__(self, show):
        # Init recognition path by LBPH Algorithm
        self.util = Utility()
        self.recognizer = cv.face.LBPHFaceRecognizer_create()
        self.recognizer.read(self.util.trainPath())

        # Initial face_cascade lib path
        self.face_cascade = cv.CascadeClassifier(self.util.HAARpath())

        print("[Initial] Face Recognition...")

        #Config font
        font = cv.FONT_HERSHEY_SIMPLEX

        # Initial camera
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 24
        rawCapture = PiRGBArray(camera, size=(640, 480))

        if camera:
            sleep(0.5)  # warmup
            print("[Initial] Camera is active...")
            print("[Initial] Look at the camera")

            # Initial id
            id = 0
            num_face = 0

            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                # flip image
                image = cv.flip(image, -1)
                # converse color to gray
                gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
                # find face by HAARCascade algorithm
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

                # draw face in image
                for (x, y, w, h) in faces:
                    cv.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                    # Check if confidence is less them 100 ==> "0" is perfect match
                    name = "unknown"
                    if (confidence < 100):
                        name = self.util.findUname(id)
                    cv.putText(image, name, (x+5, y-5), font, 1, (255, 255, 0), 2)
                    confidence_str = "{0}%".format(round(100 - confidence))
                    cv.putText(image, confidence_str, (x+5, y+h-5), font, 1, (255, 255, 0), 1)
                    if not name == "unknown":
                        print("Username : " + name + ", Confident : " + confidence_str)
                        num_face += 1
                        self.util.imageWrite(num_face, image)

                if show:
                    cv.imshow("Frame", image)

                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)

                # Exit key
                k = cv.waitKey(100) & 0xff  # Press 'ESC' for exiting video
                if k == 27:  # Create 30 face of your's images
                    print("[Closed] Camera Connection")
                    break
        else:
            print("[Error] Please check camera connection.")
        return 1
