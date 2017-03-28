import os
from tqdm import tqdm
import filecmp
from utils.helpFunctions import *
from utils.helpFunctions import *

def generatePHN(MLFfile, dstDir):
    videos = readMLFfile(MLFfile)

    for video in tqdm(videos):
            videoPath, phonemes = processVideoPhonemes(video)
            phonemes =  timeToFrame(phonemes)
            videoDir = os.path.splitext(videoPath)[0]
            videoName = os.path.basename(videoDir)
            speakerPath = os.path.dirname(os.path.dirname(os.path.dirname(videoDir)))
            speakerName = os.path.basename(speakerPath)

            if not "TCDTIMIT/" in speakerPath: raise Exception(
                "Can't extract phonemes; you have to create a 'TCDTIMIT' top level directory!!"); sys.exit(-1)
            oldStoragePath, relPath = speakerPath.split("TCDTIMIT/")  # /home/data/TCDTIMIT/volunteers/...

            # remove unneeded folders; store directly under TCDTIMIT/
            topDir = relPath.split('/')[0]
            while not (topDir == "volunteers" or topDir == "lipspeakers"):
                relPath = '/'.join(relPath.split('/')[1:])
                topDir = relPath.split('/')[0]

            storeDir = ''.join([dstDir, os.sep, relPath])
            if storeDir.endswith('/'):  storeDir = storeDir[:-1]
            storeDir = ''.join([storeDir, os.sep, videoName])

            phonemePath = ''.join([storeDir, os.sep, videoName, ".phn"])
            writeToTxt(phonemes, phonemePath)

            # print("Extracting PHN files from ", videoPath, ", saving to: \t", storeDir)
            # print phonemePath

    tcdtimitdir = os.path.dirname(os.path.dirname(speakerPath))
    return tcdtimitdir

def timeToFrame(phonemes):
    phonemeFrames = []
    for pair in phonemes:
        startFrame = int(float(pair[0]) * 16000)
        endFrame = int(float(pair[1]) * 16000)
        phoneme = pair[2]
        extractionFrame = int(float(pair[3]) * 16000)

        phonemeFrames.append( (startFrame, endFrame, phoneme)) #, extractionFrame) )  #TODO add extractionframe if extraction moment is changed for lipreading
    return phonemeFrames


if __name__ == '__main__':
    MLFfile = sys.argv[1]
    dstDir = sys.argv[2]
    generatePHN(MLFfile, dstDir)

## not needed because the files already are in the dstDir
# copyFilesOfType(tcdtimitdir, dstDir, '.phn')


## Example
# dstDir = os.path.expanduser("~/TCDTIMIT/TCDTIMITaudio")
# tcdtimitdir = generatePHN('./MLFfiles/lipspeaker_labelfiles.mlf',dstDir)
# generatePHN('./MLFfiles/volunteer_labelfiles.mlf',dstDir)


