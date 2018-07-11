# ===============================
# ====       Python 3.7      ====
# ====   Siwanont Sittinam   ====
# ==== Andon PiCamera Module ====
# ====    Face Detection     ====
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
# Import Utility
from .util import Utility

class FaceDetection:

    def __init__(self, username):
        # Name variable
        self.username = username
        if self.username is None:
            print("[Invalid Syntax] AndonCamera.faceDetection(username)")
            return None
        print("Username : " + self.username)

        # Find Path to write face images
        util = Utility()
        self.img_path_general = util.findPath(username)
        self.name_dir = util.findNameDir(username)
        if self.img_path_general is None and self.name_dir is None :
            self.name_dir = str(util.numofUser()) + "." + username
            self.img_path_general = os.path.join(util.imgRPath(), self.name_dir)
            os.mkdir(self.img_path_general)

        # Initial face_cascade lib path
        self.face_cascade = cv.CascadeClassifier(util.HAARpath())

    def camera(self):
        if not self.username is None:
            # Initial camera
            camera = PiCamera()
            camera.resolution = (640, 480)
            camera.framerate = 24
            # Initial Capture
            rawCapture = PiRGBArray(camera, size=(640, 480))

            if camera :
                sleep(0.5) # warmup
                print("[Initial] Camera is active...")
                print("[Initial] Please look at the camera and wait a minute...")

                # Initialize sampling face count
                count = 0
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
                        cv.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        count += 1
                        filename = self.name_dir + '.' + str(count) + ".jpg"
                        cv.imwrite(os.path.join(self.img_path_general, filename), gray[y:y+h, x:x+w])  # color : image[y:y+h, x:x+w]
                        print(".", end="")
                    # Uncomment if want to show the frame for debug
                    # cv.imshow("Frame", image)
                    # clear the stream in preparation for the next frame
                    rawCapture.truncate(0)

                    # Exit way
                    k = cv.waitKey(100) & 0xff  # Press 'ESC' for exiting video
                    if k == 27 or count >= 20:  # Create 30 face of your's images
                        break

                print("\n[Successful] Create " + str(count) + " images.")
                return "Successful"
            else :
                print("[Error] Please check camera connection.")
                return 0
        else:return None

    def image(self, path=None):
        if not self.username is None:
            if not path is None:
                # Init path to detect face
                list_img = os.listdir(path)
                print("[Found " + str(len(list_img)) + " images] Path : " + path)

                # Initialize sampling face count
                count = 0
                print("[Found] ", end=' ')
                # Detection Process
                for i in range(0,len(list_img)):
                    # Read File
                    img = cv.imread(os.path.join(path, list_img[i]))
                    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

                    # Face Detect
                    faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                    print(len(faces), end=' ')
                    # print("[%2d] found %d faces." % (i+1, len(faces)))

                    if len(faces) > 0:
                        # Write face
                        for (x, y, w, h) in faces:
                            count += 1
                            cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                            filename = self.name_dir + '.' + str(count) + ".jpg"
                            cv.imwrite(os.path.join(self.img_path_general, filename), gray[y:y+h, x:x+w])

                print("\n[Successful] Detect " + str(count) + " images.")
                return "Successful"
            else:
                print(
                    "[Invalid Syntax] AndonCamera.faceDetection(username).image(path=\"home/pi/image\")")
                return 0
        else:return None
