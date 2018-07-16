# ===============================
# ====       Python 3.7      ====
# ====   Siwanont Sittinam   ====
# ====       Andon Main      ====
# ===============================

from lib.andon_camera import AndonCamera
from lib.andon_voice import AndonVoice

class Andon:

    def __init__(self):
        pass

    def inputName(self):
        return input("Please input your name : ")

    def inputSource(self):
        return input("Please input source for detection [camera/image] : ")

    def inputPath(self):
        return input("Please input path for detection (if source is image) : ")

    def andonCamera(self):
        AndonCamera().faceRecognition(show=False) # show=True for debugging
        # AndonCamera().autoTraining(username=self.inputName(), source=self.inputSource(), path=self.inputPath())
        # AndonCamera().help()

    def andonVoice(self):
        AndonVoice().voiceSpeech()



