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
def processDatabase (MLFfile, storageLocation, nbThreads=2):
    print("###################################")
    videos = readMLFfile(MLFfile)
    print("There are ", len(videos), " videos to be processed...")
    framerate = 29.97
    batchSize = nbThreads  # number of videos per iteration

    detector = dlib.get_frontal_face_detector()
    predictor_path = "./shape_predictor_68_face_landmarks.dat"
    if not os.path.exists(predictor_path):
        print('Landmark predictor not found!')
    predictor = dlib.shape_predictor(predictor_path)
    
    print("This program will process all video files specified in {mlf}. It will store the extracted faces and mouths in {storageLocation}. \n \
            The process might take a while (for the lipspeaker files ~3h, for the volunteer files ~10h)".format(
        mlf=MLFfile, storageLocation=storageLocation))
    if query_yes_no("Are you sure this is correct?", "no"):
        
        batchIndex = 0
        running = 1
        # multithread the operations
        executor = concurrent.futures.ThreadPoolExecutor(nbThreads)
        
        while running:
            if batchIndex + batchSize >= len(videos):
                print("Processing LAST BATCH of videos...")
                running = 0
                currentVideos = videos[batchIndex:]  # till the end
            else:
                currentVideos = videos[batchIndex:batchIndex + batchSize]
            batchStartTime = time.clock()

            # 0. filter unused videos
            usedVideos = []
            unused = ["55F", "56M", "57M", "58F", "59F"]
            for i in range(len(currentVideos)):
                videoPath, phonemes = processVideoFile(currentVideos[i])
                if os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(videoPath)))) in unused:
                    continue
                else: usedVideos.append(currentVideos[i])
            currentVideos = usedVideos

            # 1. extract the frames
            tick = time.clock()

            futures = []
            for video in currentVideos:
                videoPath, phonemes = processVideoFile(video)
                if not os.path.exists(videoPath):
                    print("The file ", videoPath, " does not exist.")
                    logging.critical("Stopping...")
                    running = 0;
                    return -1
                videoName = os.path.splitext(os.path.basename(videoPath))[0]
                storeDir = fixStoreDirName(storageLocation, videoName, video[0])
                print("Extracting frames from ", videoPath, ", saving to: \t", storeDir)
                futures.append(
                    executor.submit(extractAllFrames, videoPath, videoName, storeDir, framerate, '1200:1000', '350:0'))
                # write phonemes and frame numbers to file
                # print("writing phonemes...")
                # speakerName = os.path.basename(os.path.dirname(storeDir))
                # futures.append(executor.submit(writePhonemesToFile,videoName, speakerName, phonemes, storeDir))
            concurrent.futures.wait(futures)
            
            print([future.result() for future in futures])
            nbVideosExtracted = sum([future.result() for future in futures])
            sleepTime = 0#nbVideosExtracted * 6
            print("Sleeping for ", sleepTime, " seconds to allow files to be written to disk.")
            time.sleep(sleepTime)  # wait till files have been written
            
            print("\tAll frames extracted.")
            print("duration: ", time.clock() - tick)
            print("----------------------------------")

            # get index of last extracted frame, as a check
            
            # if query_yes_no("stop?", "yes"): break
            
            # 2. extract the phonemes
            tick = time.clock()
            futures = []
            for video in currentVideos:
                videoPath, phonemes = processVideoFile(video)
                if not os.path.exists(videoPath):
                    print("The file ", videoPath, " does not exist.")
                    logging.critical("Stopping...")
                    running = 0;
                    return -1
                videoName = os.path.splitext(os.path.basename(videoPath))[0]
                storeDir = fixStoreDirName(storageLocation, videoName, video[0])
                print("Extracting phonemes from ", videoPath, ", saving to: \t", storeDir)
                # write phonemes and frame numbers to file
                speakerName = os.path.basename(os.path.dirname(storeDir))
                futures.append(executor.submit(writePhonemesToFile, videoName, speakerName, phonemes, storeDir))
            concurrent.futures.wait(futures)
            print("phonemes have been written")
            print("duration: ", time.clock() - tick)
            print("-----------------------------")
            
            # 2. remove unneccessary frames
            tick = time.clock()
            futures = []
            for video in currentVideos:
                videoPath, phonemes = processVideoFile(video)
                videoName = os.path.splitext(os.path.basename(videoPath))[0]
                videoDir = fixStoreDirName(storageLocation, videoName, video[0])
                print("removing invalid frames from ", storeDir)
                futures.append(executor.submit(deleteUnneededFiles, videoDir))
            concurrent.futures.wait(futures)

            nbRemoved = sum([future.result() for future in futures])
            print("there were ", nbRemoved, "frames removed")
            print("\tAll unnecessary frames removed.")
            print("duration: ", time.clock() - tick)
            print("----------------------------------")
            sleepTime = nbRemoved * 0.015
            time.sleep(sleepTime)
            
            # 3. extract faces and mouths
            tick = time.clock()
            futures = []
            for video in currentVideos:
                videoPath, phonemes = processVideoFile(video)
                videoName = os.path.splitext(os.path.basename(videoPath))[0]
                sourceDir = fixStoreDirName(storageLocation, videoName, video[0])
                storeDir = sourceDir
                print("Extracting faces from ", sourceDir)
                # exectute. The third argument is the path to the dlib facial landmark predictor
                futures.append(executor.submit(extractFacesMouths, sourceDir, storeDir, detector, predictor))
            concurrent.futures.wait(futures)
            print("\tAll faces and mouths have been extracted.")
            print("duration: ", time.clock() - tick)
            print("----------------------------------")
            
            # 4. convert to grayscale
            tick = time.clock()
            futures = []
            for video in currentVideos:
                videoPath, phonemes = processVideoFile(video)
                videoName = os.path.splitext(os.path.basename(videoPath))[0]
                sourceDir = fixStoreDirName(storageLocation, videoName, video[0])
                storeDir = sourceDir
                dirNames = ["faces", "mouths"]
                print("Converting to grayscale from: ", sourceDir)
                futures.append(executor.submit(convertToGrayScale, sourceDir, dirNames))
            concurrent.futures.wait(futures)
            print("\tAll faces and mouths have been converted to grayscale.")
            print("duration: ", time.clock() - tick)
            print("----------------------------------")
            
            # 5. resize mouth images, for convnet usage
            tick = time.clock()
            futures = []
            for video in currentVideos:
                videoPath, phonemes = processVideoFile(video)
                videoName = os.path.splitext(os.path.basename(videoPath))[0]
                # storeDir: eg /home/data/TCDTIMIT/processed/lipspeakers/LipSpkr1/sa1
                storeDir = fixStoreDirName(storageLocation, videoName, video[0])
                rootDir = storeDir
                dirNames = ["mouths_gray", "faces_gray"]
                print("Resizing images from: ", sourceDir)
                futures.append(executor.submit(resizeImages, storeDir, dirNames, False, 120.0))
            concurrent.futures.wait(futures)
            print("\tAll mouths have been resized.")
            print("duration: ", time.clock() - tick)
            print("----------------------------------")

            batchDuration = time.clock() - batchStartTime
            print("#####################################")
            print("\t Batch Done!     duration: ", batchDuration)
            print("#####################################")
            
            # update the batchIndex
            batchIndex += batchSize
        
        print("All done.")
    else:
        print("Okay then, goodbye!")
    return 0
