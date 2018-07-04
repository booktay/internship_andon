# ===============================
# ====       Python 3.7      ====
# ====   Siwanont Sittinam   ====
# ====      Andon Camera     ====
# ===============================

from lib.face_detection import FaceDetection
from lib.face_training import FaceTraining
from lib.face_recognition import FaceRecognition

class AndonCamera:

    def __init__(self):
        pass

    def faceDetection(self, username=None):
        return FaceDetection(username)

    def faceTraining(self, username=None, all=True):
        return FaceTraining(username, all)

    def faceRecognition(self, show=False):
        return FaceRecognition(show)

    def autoTraining(self, username=None, source=None, path=None):
        print("[Initial] Start auto program...")
        if source == "camera": FaceDetection(username).camera()
        elif source == "image" and not path is None : FaceDetection(username).image(path)
        else :
            print("[Invalid Syntax] AndonCamera.autoTraining(username=\"username\", source=\"image\", path=\"/home/pi/image/name\")")
            return None
        FaceTraining().LBPHtrain()

    def help(self):
        print("====================================== Manual AndonCamera() ======================================")
        print("  ## Auto Program ##                                                                                  ")
        print("  AndonCamera().autoTraining(username=\"username\", source=\"camera\")                                ")
        print("  AndonCamera().autoTraining(username=\"username\", source=\"image\", path=\"/home/pi/image/name\")   ")
        print("  # source for use camera or images for detection                                                     ")
        print("  ## Face Detection ##                                                                                ")
        print("  AndonCamera().faceDetection(\"username\").camera()                                                  ")
        print("  # .camera() for use camera for detection                                                            ")
        print("  AndonCamera().faceDetection(\"username\").image(\"/home/pi/image\")                                 ")
        print("  # .image(path) for use image for detection                                                          ")
        print("  ## Face Training ##                                                                                 ")
        print("  AndonCamera().faceTraining().LBPHtrain() -> Default algorithm                                       ")
        print("  # .LBPHtrain() : LBPH Algorithm                                                                     ")
        print("  AndonCamera().faceTraining().Eigentrain()                                                           ")
        print("  # .Eigentrain() : Eigen Algorithm                                                                   ")
        print("  AndonCamera().faceTraining().Fishertrain()                                                          ")
        print("  # .Fishertrain() : Fisher Algorithm                                                                 ")
        print("  ## Face Recognition ##                                                                              ")
        print("  AndonCamera().faceRecognition(show=True) -> show=True : Show gui                                    ")
        print("==================================================================================================")
        return "Help"
