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
from util import Utility
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
        if user :
            return user
        return None

    def updateUser(self, username):
        user = self.user.updateOne({
            {
                'username': username
            },{
                '$set': {"password": "simple", "git": "https://github.com/simple/my_page"},
                '$currentDate': {'lastModified': True}
            }
        })


pp.pprint(DatabaseConnection().updateUser("test"))

