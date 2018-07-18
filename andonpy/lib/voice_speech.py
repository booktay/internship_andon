#!/usr/bin/env python
# Siwanont Sittinam
# Speech

# Import management linux system module
import sys as sys
import os as os
import speech_recognition as sr
from utility import Utility

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
                pass