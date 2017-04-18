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
        frame = int(np.round(time * framerate))
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


storageLocation = os.path.expanduser("~/TCDTIMIT/extracted")
if not os.path.exists(storageLocation): os.makedirs(storageLocation)
video = readMLFfile('/home/matthijs/Desktop/sx180.phn')[0]

videoPath, phonemes = processVideoFile(video)
if not os.path.exists(videoPath):
    print("The file ", videoPath, " does not exist.")
    pdb.set_trace()

print(phonemes)
pdb.set_trace()

videoName = os.path.splitext(os.path.basename(videoPath))[0]
storeDir = fixStoreDirName(storageLocation, videoName, video[0])
print("Extracting phonemes from ", videoPath, ", saving to: \t", storeDir)

# write phonemes and frame numbers to file
speakerName = os.path.basename(os.path.dirname(storeDir))
writePhonemesToFile2(videoName, speakerName, phonemes, storeDir)