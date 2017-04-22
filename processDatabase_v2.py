# from http://stackoverflow.com/questions/10672578/extract-video-frames-in-python#10672679

# Goal: parametrized, automated version of
#       ffmpeg -i in.mp4 -ss 00:00:20 -s 120x120 -r 1 -f singlejpeg myframe.jpg
from __future__ import print_function

import logging
import time

import concurrent.futures

from utils.helpFunctions import *


#####################################
########### Main Function  ##########
#####################################

### Executing ###
def processDatabase(MLFfile, storageLocation, nbThreads=2):
    print("###################################")
    videos = readMLFfile(MLFfile)
    print("There are ", len(videos), " videos to be processed...")
    framerate = 29.97
    batchSize = nbThreads  # number of videos per iteration

    saveFaces = True
    saveMouths = True

    detector = dlib.get_frontal_face_detector()
    predictor_path = "./shape_predictor_68_face_landmarks.dat"
    if not os.path.exists(predictor_path):
        print('Landmark predictor not found!')
    predictor = dlib.shape_predictor(predictor_path)

    print("This program will process all video files specified in {mlf}. It will store the extracted faces and mouths in {storageLocation}. \n \
            The process might take a while (for the lipspeaker files ~3h, for the volunteer files ~10h)".format(
            mlf=MLFfile, storageLocation=storageLocation))

    if True:  # query_yes_no("Are you sure this is correct?", "no"):

        # multithread the operations
        executor = concurrent.futures.ThreadPoolExecutor(nbThreads)
        badVideos = []

        for video in videos:
            executor.submit(processVideo, badVideos, detector, framerate, predictor, saveFaces, saveMouths, storageLocation, video, verbose=False)

        print("All done.")
        executor.shutdown(wait=True)
    else:
        print("Okay then, goodbye!")
    return 0


def processVideo(badVideos, detector, framerate, predictor, saveFaces, saveMouths, storageLocation, video, verbose=True):
    videoStartTime = time.clock()
    # 0. filter unused videos
    unused = ["55F", "56M", "57M", "58F", "59F"]
    videoPath, phonemes = processVideoFile(video)
    if os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(videoPath)))) in unused:
        return videoPath
    if not os.path.exists(videoPath):
        logging.error("The file ", videoPath, " does not exist.")
        return videoPath

    # 0b. get video information
    videoName = os.path.splitext(os.path.basename(videoPath))[0]
    storeDir = fixStoreDirName(storageLocation, videoName,
                               video[0])  # eg /home/data/TCDTIMIT/processed/lipspeakers/LipSpkr1/sa1
    speakerName = os.path.basename(os.path.dirname(storeDir))

    # 1. extract the frames
    tick = time.clock()
    if verbose: print("Extracting frames from ", videoPath, ", saving to: \t", storeDir)
    extractAllFrames(videoPath, videoName, storeDir, framerate, '1200:1000', '350:0')
    if verbose:
        print("\tAll frames extracted.")
        print("duration: ", time.clock() - tick)
        print("----------------------------------")

    # 2. extract the phonemes
    tick = time.clock()
    if verbose: print("Extracting phonemes from ", videoPath, ", saving to: \t", storeDir)
    # write phonemes and frame numbers to file
    writePhonemesToFile(videoName, speakerName, phonemes, storeDir)
    if verbose:
        print("phonemes have been written")
        print("duration: ", time.clock() - tick)
        print("-----------------------------")

    # 2. remove unneccessary frames
    tick = time.clock()
    videoName = os.path.splitext(os.path.basename(videoPath))[0]
    if verbose: print("removing invalid frames from ", storeDir)
    nbRemoved = deleteUnneededFiles(storeDir)
    if verbose:
        print("there were ", nbRemoved, "frames removed")
        print("\tAll unnecessary frames removed.")
        print("duration: ", time.clock() - tick)
        print("----------------------------------")
    sleepTime = nbRemoved * 0.015
    time.sleep(sleepTime)

    # 3. extract faces and mouths
    tick = time.clock()
    sourceDir = storeDir
    if verbose: print("Extracting faces from ", sourceDir)
    extractFacesMouths(sourceDir, storeDir, detector, predictor, saveFaces, saveMouths)
    if verbose:
        print("\tAll faces and mouths have been extracted.")
        print("duration: ", time.clock() - tick)
        print("----------------------------------")

    # 4. resize mouth images, for convnet usage: 120x120
    tick = time.clock()
    dirNames = []
    if saveMouths: dirNames.append("mouths")
    if saveFaces: dirNames.append("faces")  # dirNames = ["mouths_gray", "faces_gray"]
    if verbose: print("Resizing images from: ", sourceDir)
    resizeImages(storeDir, dirNames, False, 120.0)
    if verbose:
        print("\tAll mouths have been resized.")
        print("duration: ", time.clock() - tick)
        print("----------------------------------")
    videoDuration = time.clock() - videoStartTime

    print("\t Video ", videoName, " Done!     duration: ", videoDuration)
    if verbose: print("#####################################")

    return None
