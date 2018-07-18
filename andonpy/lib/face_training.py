# ===============================
# ====       Python 3.7      ====
# ====   Siwanont Sittinam   ====
# ==== Andon PiCamera Module ====
# ====     Face Training     ====
# ===============================

# Import management linux system module
import sys
import os
# Import image processing module
import cv2 as cv
import numpy as np
from PIL import Image
from utility import Utility

class FaceTraining:

    def __init__(self, username=None, all=True):
        # Name variable
        self.username = username
        self.all = all
        if self.all and not self.username is None:
            print("[Invalid Syntax] AndonCamera.faceTraining(username, all=False)")
            print("[Invalid Syntax] -------------------- OR ---------------------")
            print("[Invalid Syntax] AndonCamera.faceTraining()")
            return None
        elif self.all and self.username is None:
            print("[Training] All")
        elif not self.all and not self.username is None:
            print("[Training] Username : " + self.username)

        # Find Path to write face images
        self.util = Utility()
        self.path_all = self.util.allPath()
        self.name_dir = self.util.allUser()
        self.name_id = self.util.allID()

        #Set Train Path
        self.train_path = self.util.trainPath()

        # Initial face_cascade lib path
        self.face_cascade = cv.CascadeClassifier(self.util.HAARpath())

    def makelabel(self):
        faces_all = []
        id_all = []
        if (not self.all and self.username is None) or (self.all and not self.username is None):
            return None
        print("[Initial] Making Label...")
        if not self.username is None and not self.all:
            path = self.util.findPath(self.username)
            img_in_path = self.util.findImginDir(self.username)
            if not img_in_path is None:
                for img_in_dir in img_in_path:
                    img_PIL = Image.open(img_in_dir).convert('L')
                    img_group = np.array(img_PIL, 'uint8')
                    id = self.util.findID(self.username)
                    faces = self.face_cascade.detectMultiScale(img_group)
                    for (x, y, w, h) in faces:
                        faces_all.append(img_group[y:y+h, x:x+w])
                        id_all.append(int(id))
                return faces_all, id_all
            else:return None
        elif self.username is None and self.all:
            all_path = self.util.allPath()
            all_id = self.util.allID()
            all_user = self.util.allUser()
            for order in range(1, len(all_path)):
                for img_in_dir in self.util.findallImgDir(all_path[order]):
                    img_PIL = Image.open(img_in_dir).convert('L')
                    img_group = np.array(img_PIL, 'uint8')
                    faces = self.face_cascade.detectMultiScale(img_group)
                    for (x, y, w, h) in faces:
                        faces_all.append(img_group[y:y+h, x:x+w])
                        id_all.append(int(all_id[order]))
                print("[Label] " + all_user[order])
            return faces_all, id_all
        else : return None

    def LBPHtrain(self):
        if (not self.all and self.username is None) or (self.all and not self.username is None):
            return None
        print("[Initial] LBPH Training faces. It will take a few seconds. Wait...")
        face, ids = self.makelabel()
        recognizer = cv.face.LBPHFaceRecognizer_create()
        recognizer.train(face, np.array(ids))
        train_name = self.util.trainPath()
        if not self.username is None and not self.all:
            train_name = self.util.findID(self.username) + "." + self.username + ".yml"
        recognizer.write(os.path.join(self.train_path, train_name))
        print("[Successful] Faces training")
        return "Successful"

    def Eigentrain(self):
        if (not self.all and self.username is None) or (self.all and not self.username is None):
            return None
        print("[Initial] LBPH Training faces. It will take a few seconds. Wait...")
        face, ids = self.makelabel()
        recognizer = cv.face.EigenFaceRecognizer_create()
        recognizer.train(face, np.array(ids))
        train_name = self.util.trainPath()
        if not self.username is None and not self.all:
            train_name = self.util.findID(self.username) + "." + self.username + ".yml"
        recognizer.write(os.path.join(self.train_path, train_name))
        print("[Successful] Faces training")
        return "Successful"

    def Fishertrain(self):
        if (not self.all and self.username is None) or (self.all and not self.username is None):
            return None
        print("[Initial] LBPH Training faces. It will take a few seconds. Wait...")
        face, ids = self.makelabel()
        recognizer = cv.face.FisherFaceRecognizer_create()
        recognizer.train(face, np.array(ids))
        train_name = self.util.trainPath()
        if not self.username is None and not self.all:
            train_name = self.util.findID(self.username) + "." + self.username + ".yml"
        recognizer.write(os.path.join(self.train_path, train_name))
        print("[Successful] Faces training")
        return "Successful"
