#!/usr/bin/env python
# Siwanont Sittinam
# Training dataset

import sys as sys
import os as os
import cv2 as cv

from .utility import Utility
util = Utility()

face_cascade = cv.CascadeClassifier(util.HAARPath())

import numpy as np
from PIL import Image

class Training:

    def __init__(self, all=True):
        self.all = all

        # Name variable
        self.face_cascade = cv.CascadeClassifier(util.HAARPath())

    def makelabel(self):
        if not self.all:return None

        print("[Process] Making Label")
        faces_all = []
        id_all = []

        user = util.User()
        for u in range(1,len(user)):
            img = util.UserIMG(user[u][1])
            if img:
                for path in img:
                    img_PIL = Image.open(path).convert('L')
                    img_np = np.array(img_PIL, 'uint8')
                    faces = face_cascade.detectMultiScale(img_np)
                    for (x, y, w, h) in faces:
                        faces_all.append(img_np[y:y+h, x:x+w])
                        id_all.append(int(user[u][0]))
        return faces_all, id_all

    def train(self):
        print("[Process] Training faces. It will take a few minutes. Wait...")
        train_path = util.TRAINPath()
        print("[Process] Training...")
        face, ids = self.makelabel()
        recognizer_lbph = cv.face.LBPHFaceRecognizer_create()
        recognizer_lbph.train(face, np.array(ids))
        recognizer_lbph.write(train_path[0])
        print("[Successful] Faces training")
        return 1
