#!/usr/bin/env python
# Siwanont Sittinam
# Config

# Import necessary module
import os as os
import urllib.parse as parse

# MONGODB
USERNAME = parse.quote_plus('pi')
PASSWORD = parse.quote_plus('p1p1p1p1')
URL = '@ds219191.mlab.com:19191/'
DATABASE_NAME = 'andon'
COLLECTION_NAME = 'user'
MONGO_PATH = 'mongodb://%s:%s%s%s' % (USERNAME, PASSWORD, URL, DATABASE_NAME)

# PATH
ROOT_PATH = os.path.join("/home/pi/","internship_andon")
IMG_STD_PATH = os.path.join(ROOT_PATH,"image")
EXAMPLE_PATH = os.path.join(IMG_STD_PATH,"example")
TRAIN_PATH_MAIN_YML = os.path.join(IMG_STD_PATH, "trainer.yml")
