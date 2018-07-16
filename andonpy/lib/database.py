# ===============================
# ====       Python 3.7      ====
# ====   Siwanont Sittinam   ====
# ==== Andon PiCamera Module ====
# == Face Database Connection  ==
# ===============================

# Import management linux system module
import sys
import os
import pprint as pp
from .util import Utility
from pymongo import MongoClient

try:
   from config import MONGO_PATH
except ImportError:
   pass

class DatabaseConnection:

    def __init__(self):
        # Init recognition path by LBPH Algorithm
        self.util = Utility()
        self.db_con = MongoClient(MONGO_PATH)
        self.user = self.db_con['andon']['user']

    def getUser(self, username):
        user = self.user.find_one({'username':username})
        if user : return user
        return None

    def getallUser(self, fields):
        projection = {
            '$project': { fields : 1, "status" : 1 }
        }
        user = self.user.aggregate([projection])
        if user : return user
        return None

    def updateStatusUser(self, username, state=True):
        want_to_update = {
            "status": state
        }
        res = self.user.update_one({'username': username}, {"$set": want_to_update})
        return res.modified_count
