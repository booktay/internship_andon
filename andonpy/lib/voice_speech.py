# ===============================
# ====       Python 3.7      ====
# ====   Siwanont Sittinam   ====
# ==== Andon PiCamera Module ====
# ====    Voice to Speech    ====
# ===============================

# Import management linux system module
import sys
import os
import speech_recognition as sr
from util import Utility

class VoiceSpeech:

    def __init__(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something")
            audio = r.listen(source)
            print("Process")

            try:
                print("Text : " + r.recognize_google(audio))
            except:
                print("...")
                pass

VoiceSpeech()