import time

# relPath = "test/dir/dir2/volunteers/Lipspkr1/sa1/sa1.phn"
# topDir = relPath.split('/')[0]
# print topDir
# while not (topDir == "volunteers" or topDir == "lipspeakers"):
#     relPath = '/'.join(relPath.split('/')[1:])
#     topDir = relPath.split('/')[0]
#
#     print relPath, topDir
#     time.sleep(0.5)
# print relPath

import os
from utils.removeEmptyDirs import *
from fixTCDTIMITwavStructure import *
from getPhnFiles import *

# dstDir = os.path.expanduser("~/TCDTIMIT/TCDTIMITaudio")
#
# ## PHN: generate phoneme files
# print("EXTRACTING PHNS...")
# print("lipspeakers:")
# generatePHN("MLFfiles/lipspeaker_labelfiles.mlf", dstDir)
# print("volunteers:")
# generatePHN("MLFfiles/volunteer_labelfiles.mlf", dstDir)

import pdb
# some phonemes are skipped??
# videos = readMLFfile("MLFfiles/lipspeaker_labelfiles.mlf")
# for video in videos[0:10]:
#     videoPath, phonemes = processVideoFile(video)
#     pdb.set_trace()

from utils.helpFunctions import *
# get valid times, phonemes, frame numbers
def getValid(time_phonemes, framerate):  # frameRate = 29.97 for the TCDTimit database
    import math
    # take care of duplicates: loop through the phonemes, if two are same frame, only keep the first one
    seen_framePhonemes = set()
    validFrames = []
    validPhonemes = []
    validTimes = []
    for time_phoneme in time_phonemes:
        time = float(time_phoneme[0])
        frame = int(math.floor(time * framerate))
        phoneme = time_phoneme[1]
        if (frame, phoneme) not in seen_framePhonemes:
            validPhonemes.append(time_phoneme[1])
            validTimes.append(time)
            validFrames.append(frame)
            seen_framePhonemes.add(frame)
        else:
            print("frame_phoneme ", (frame, phoneme), " already seen")
    return validTimes, validFrames, validPhonemes


# write file with phonemes and corresponding frame numbers. First column = frames. Second column = corresponding phonemes
def writePhonemesToFile2(videoName, speakerName, phonemes, targetDir):
    validTimes, validFrames, validPhonemes = getValid(phonemes, 29.97)
    phonemeFile = ''.join([targetDir, os.sep, speakerName, "_", videoName, "_PHN.txt"])
    if not os.path.exists(targetDir): os.makedirs(targetDir)

    # add 1 to the validFrames to fix the ffmpeg issue (starts at 1 instead of 0)
    for i in range(0, len(validFrames)):
        validFrames[i] += 1
        if validFrames[i] <1: validFrames[i]=1

    pdb.set_trace()

    # check that no frames are larger than last frame extracted by extractAllFrames
    highest = 1
    for root, dirs, files in os.walk(targetDir):
        for file in files:
            name, ext = os.path.splitext(file)
            if not ext ==".jpg": continue
            frame = int(name.split("_")[1])
            if frame > highest: highest = frame

    for i in range(len(validFrames)):
        if validFrames[i] > highest:
            print("FOUND HIGHER THAN HIGHEST:", validFrames[i])
            validFrames[i] = highest

    pdb.set_trace()

    # write to text file
    thefile = open(phonemeFile, 'w')
    for i in range(len(validFrames) - 1):
        item = (validFrames[i], validPhonemes[i])
        thefile.write(' '.join(map(str, item)) + "\r\n")
    item = (validFrames[-1], validPhonemes[-1])
    thefile.write(' '.join(map(str, item)))
    thefile.close()

    # also write a mat file
    matPath = targetDir + os.sep + "phonemeFrames.mat"
    sio.savemat(matPath, {'validFrames': np.array(validFrames), 'validPhonemes': np.array(validPhonemes)})

    return 0

def deleteUnneededFiles(videoDir):
    print("deleting files...")
    # read correct frames: firs column of text file
    parentName = os.path.basename(os.path.dirname(videoDir))
    dirName = os.path.basename(videoDir)
    validFrames = []
    with open(videoDir + os.sep + parentName + "_" + dirName + "_PHN.txt") as inf:
        for line in inf:
            parts = line.split()  # split line into parts
            if len(parts) > 1:  # if at least 2 parts/columns
                validFrames.append(parts[0])  # print column 2

    import pdb;pdb.set_trace()
    # walk through the files, if a file doesn't contain '_validFrame', then remove it.
    nbRemoved = 0
    for root, dirs, files in os.walk(videoDir):
        files.sort(key=tryint)
        for f in files:
            name, ext = os.path.splitext(f)
            filePath = os.path.join(root, f)
            if ext != ".jpg": remove = 0; continue
            fname = os.path.splitext(f)[0]
            fnumber = fname.split("_")[1]
            if fnumber not in validFrames:
                os.remove(filePath)
                nbRemoved += 1

    return nbRemoved


detector = dlib.get_frontal_face_detector()
predictor_path = "./shape_predictor_68_face_landmarks.dat"
if not os.path.exists(predictor_path):
    print('Landmark predictor not found!')
predictor = dlib.shape_predictor(predictor_path)



storageLocation = os.path.expanduser("~/TCDTIMIT/extracted")
if not os.path.exists(storageLocation): os.makedirs(storageLocation)
video1 = readMLFfile('/home/matthijs/Desktop/si2246.phn')[0]
video2 = readMLFfile('/home/matthijs/Desktop/sx180.phn')[0]
video3 = readMLFfile('/home/matthijs/Desktop/sx343.phn')[0]

videos = [video1]#,video2,video3]

for video in videos:
    videoPath, phonemes = processVideoFile(video)
    print(videoPath)
    if not os.path.exists(videoPath):
        print("The file ", videoPath, " does not exist.")
        #pdb.set_trace()

    print(phonemes)

    videoName = os.path.splitext(os.path.basename(videoPath))[0]
    storeDir = fixStoreDirName(storageLocation, videoName, video[0])
    print("Extracting phonemes from ", videoPath, ", saving to: \t", storeDir)


    framerate = 29.97
    extractAllFrames(videoPath, videoName, storeDir, framerate, '1200:1000', '350:0')

    # write phonemes and frame numbers to file
    speakerName = os.path.basename(os.path.dirname(storeDir))
    writePhonemesToFile2(videoName, speakerName, phonemes, storeDir)

    videoDir = fixStoreDirName(storageLocation, videoName, video[0])
    a = deleteUnneededFiles(videoDir)


    sourceDir = fixStoreDirName(storageLocation, videoName, video[0])
    extractFacesMouths(sourceDir, storeDir, detector, predictor)

    dirNames = ["faces", "mouths"]
    convertToGrayScale(sourceDir, dirNames)

    dirNames = ["mouths_gray", "faces_gray"]
    storeDir = fixStoreDirName(storageLocation, videoName, video[0])
    resizeImages(storeDir, dirNames, False, 120.0)

    print("deleted: ", a)

