#!/usr/bin/env python
# Siwanont Sittinam
# Utility

# Import necessary modules
import sys as sys
import os as os
import cv2 as cv
import pprint as pp
from pymongo import MongoClient
import netifaces as netif

# Import environment variables
try:
   from .config import IMG_STD_PATH, TRAIN_LBPH_YML, TRAIN_EIGE_YML, TRAIN_FICH_YML, MONGO_PATH, DATABASE_NAME, COLLECTION_NAME
except ImportError:
   pass

class Utility:

    def __init__(self):
        self.HAAR_PATH = os.popen("find /usr -name haarcascade_frontalface_default.xml -print -quit").read().split('\n')[0]
        self.DB_CONNECTION = MongoClient(MONGO_PATH)
        self.COLLECTION = self.DB_CONNECTION[DATABASE_NAME][COLLECTION_NAME]

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
        for interface in netif.interfaces():
            ip = netif.ifaddresses(interface)
            if 2 in ip.keys():
                ALL_IP.append([interface,ip[2][0]['addr']])
        return ALL_IP

    # Mongo
    def getUser(self, username=None, id=None):
        QUERY = {}
        if not id is None:
            QUERY['id'] = id
        elif not username is None:
            QUERY['username'] = username.lower()
        DOCUMENT = self.COLLECTION.find_one(QUERY)
        if DOCUMENT : return DOCUMENT
        return None

    def allUser(self, fields=None):
        QUERY = {}
        if not fields is None:
            QUERY['$project'] = {fields: 1, "status": 1}
        ALL_USER = self.COLLECTION.aggregate([QUERY])
        if ALL_USER : return ALL_USER
        return None

    def updateUser(self, username=None, status=True):
        QUERY = {
            "status": status
        }
        res = self.COLLECTION.update_one({'username': username}, {"$set": QUERY})
        return res.modified_count