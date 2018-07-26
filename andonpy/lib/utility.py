#!/usr/bin/env python
# Siwanont Sittinam
# Utility

# Import necessary modules
import sys as sys
import os as os
import cv2 as cv
import pprint as pp

import netifaces as netifaces
import requests

# PATH
ROOT_PATH = os.path.join("/home/pi/", "internship_andon")
IMG_STD_PATH = os.path.join(ROOT_PATH, "image")
EXAMPLE_PATH = os.path.join(IMG_STD_PATH, "example")
TRAIN_PATH = os.path.join(ROOT_PATH, "train")
TRAIN_LBPH_YML = os.path.join(TRAIN_PATH, "lbph.yml")
TRAIN_EIGE_YML = os.path.join(TRAIN_PATH, "eige.yml")
TRAIN_FICH_YML = os.path.join(TRAIN_PATH, "fich.yml")

class Utility:

    def __init__(self):
        self.HAAR_PATH = os.popen("find /usr -name haarcascade_frontalface_default.xml -print -quit").read().split('\n')[0]

    def HAARPath(self):
        return self.HAAR_PATH

    def IMGROOTPath(self):
        return IMG_STD_PATH

    def TRAINPath(self):
        return [TRAIN_LBPH_YML, TRAIN_EIGE_YML, TRAIN_FICH_YML]

    def User(self):
        NAMES = sorted([name.split('.') for name in os.listdir(IMG_STD_PATH)])
        for NAME in NAMES:
            NAME.append(os.path.join(IMG_STD_PATH, ".".join(str(N) for N in NAME)))
        return NAMES

    def numUser(self):
        return len(os.listdir(IMG_STD_PATH))

    def haveUser(self, USERNAME="unknown"):
        NAMES = self.User()
        for NAME in NAMES:
            if USERNAME.lower() == NAME[1].lower():
                return NAME
        return NAMES[0]

    def UserIMG(self, USERNAME="unknown"):
        PATH = self.haveUser(USERNAME.lower())
        if not PATH[0] is '0':
            return sorted([os.path.join(PATH[2], NAME) for NAME in os.listdir(PATH[2])])
        return None

    def writeIMG(self, path=IMG_STD_PATH, name="unknown", file=None, type="jpg"):
        if not file is None:
            SAVE_PATH = os.path.join(path, name.lower() + "." + type.lower())
            return cv.imwrite(SAVE_PATH, file)
        return None

    def getIP(self):
        ALL_IP = []
        print('[Initial] Recognition with camera')
        port = 5001
        for interface in netifaces.interfaces():
            ip = netifaces.ifaddresses(interface)
            try:
                print("[Initial]  * Running on http://" + ip[2][0]['addr'] + ":" + str(port) + "/ for interfaces " + interface)
            except:
                pass
        print("[Initial] Please open the following link.")

    # MongoDB using API NodeJS
    def reqRes(self, username = None):
        if username is None:
            return "Not found"
        ip = "http://localhost:5000/api/user/updateDB"
        return requests.post(ip, data={'username': username}).json()
