# ===============================
# ====       Python 3.7      ====
# ====   Siwanont Sittinam   ====
# ==== Andon PiCamera Module ====
# ====        Utility        ====
# ===============================

# Import management linux system module
import sys
import os
# Use CV2
import cv2 as cv

try:
   from config import IMG_STD_PATH, TRAIN_PATH, EXAMPLE_PATH, TRAIN_PATH_MAIN_YML
except ImportError:
   pass

class Utility:

    def __init__(self):
        pass

    def findIndexUser(self, username):
        uname_all = sorted([name.split('.')[1] for name in os.listdir(IMG_STD_PATH)])
        if username in uname_all:
            return uname_all.index(username)
        return None

    def findUname(self, id):
        uname_all=sorted([name.split('.')[1] for name in os.listdir(IMG_STD_PATH)])
        id_all = sorted([name.split('.')[0] for name in os.listdir(IMG_STD_PATH)])
        if str(id) in id_all:
            return uname_all[id_all.index(str(id))]
        return None

    def findID(self, username):
        id_all = sorted([name.split('.')[0] for name in os.listdir(IMG_STD_PATH)])
        if not self.findIndexUser(username) is None:
            return id_all[self.findIndexUser(username)]
        return None

    def findNameDir(self, username):
        name_dir_all = sorted([name for name in os.listdir(IMG_STD_PATH)])
        if not self.findIndexUser(username) is None:
            return name_dir_all[self.findIndexUser(username)]
        return None

    def findPath(self, username):
        path_all = sorted([os.path.join(IMG_STD_PATH, name) for name in os.listdir(IMG_STD_PATH)])
        if self.findIndexUser(username):
            return path_all[self.findIndexUser(username)]
        return None

    def findImginDir(self, username):
        path = self.findPath(username)
        if not path is None:
            return sorted([os.path.join(path, name) for name in os.listdir(path)])
        return None

    def findallImgDir(self, path):
        if not path is None:
            return sorted([os.path.join(path, name) for name in os.listdir(path)])
        return None

    def allID(self):
        return sorted([name.split('.')[0] for name in os.listdir(IMG_STD_PATH)])

    def allUser(self):
        return sorted([name.split('.')[1] for name in os.listdir(IMG_STD_PATH)])

    def allNameDir(self):
        return sorted([name for name in os.listdir(IMG_STD_PATH)])

    def allPath(self):
        return sorted([os.path.join(IMG_STD_PATH, name) for name in os.listdir(IMG_STD_PATH)])

    def numofUser(self):
        return len([name for name in os.listdir(IMG_STD_PATH)])

    def imgRPath(self):
        return IMG_STD_PATH

    def trainPath(self):
        return TRAIN_PATH_MAIN_YML

    def HAARpath(self):
        return os.popen("find /usr -name haarcascade_frontalface_default.xml -print -quit").read().split('\n')[0]

    def imageWrite(self, num, img):
        return cv.imwrite(os.path.join(EXAMPLE_PATH, str(num).format("%2d") + ".jpg"), img)


