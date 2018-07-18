#!/usr/bin/env python
# Siwanont Sittinam
# Face Main Command

# Import necessary modules
import optparse as optparse
import sys as sys
# from lib.face_detection import FaceDetection
# from lib.face_training import FaceTraining

from lib.create_dataset  import app
from lib.utility import Utility
util = Utility()

def whenError(parser):
    parser.print_help()
    sys.exit(1)

def createDataset(source):
    source = source.lower()
    print('[Initial] create dataset')
    # FD = FaceDetection()
    if source == "camera":
        print('[Initial] detect faces with camera')
        for ip in util.getIP():
            print("[Initial] Running on http://"+ ip[1] + ":5000/ for interfaces " + ip[0])
        app.run(host='0.0.0.0', threaded=True)
    elif source == "image":
        print('[Initial] detect faces with image')
        # name = input('[Initial] Input username : ')
        # FD.image()
        print("Coming soon")

def trainDataset():
    print('[Initial] train all datasets')
    # FT = FaceTraining()

def main():
    parse = optparse.OptionParser()
    parse.add_option('-c', '--create', default=False, action="store_true" , help="create dataset", dest="create")
    parse.add_option('-t', '--train', default=False, action="store_true" , help="train all datasets", dest="train")
    parse.add_option('-a', '--auto', default=False, action="store_true" , help="use camera to create dataset and train all datasets", dest="auto")
    create_group = optparse.OptionGroup(parse, "Creating Dataset Options", "Use These Options with -c, --create for Creating dataset")
    create_group.add_option('--source', help="choose camera or image to create datasets", dest="source", type="string")
    parse.add_option_group(create_group)
    options, arguments = parse.parse_args()

    if options.auto and not options.create and not options.train:
        print("[Initial] Auto mode")
        print("[Initial] Creating dataset by camera and Training all datasets")
        createDataset(source="camera")
        trainDataset()
    elif options.create and not options.train and not options.auto:
        if options.source : createDataset(options.source)
        else : whenError(parse)
    elif options.train and not options.create and not options.auto:
        if options.source : whenError(parse)
        else : trainDataset()
    else : whenError(parse)

if __name__ == '__main__':
    main()
