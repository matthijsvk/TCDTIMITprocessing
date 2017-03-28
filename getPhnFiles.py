from helpFunctions import *
import os

from copyFilesOfType import *

def generatePHN(MLFfile, dstDir):
    videos = readMLFfile(MLFfile)

    i=0
    for video in videos:
        if i==0:
            videoPath, phonemes = processVideoPhonemes(video)
            phonemes=  timeToFrame(phonemes)
            videoDir = os.path.splitext(videoPath)[0]
            videoName = os.path.basename(videoDir)
            speakerPath = os.path.dirname(os.path.dirname(os.path.dirname(videoDir)))
            speakerName = os.path.basename(speakerPath)

            storeDir = fixStoreDirName(dstDir, videoName, video[0])
            # speakerName = os.path.basename(os.path.dirname(storeDir))
            print("Extracting PHN files from ", videoPath, ", saving to: \t", storeDir)

            phonemePath = ''.join([storeDir, os.sep, videoName, ".phn"]) #speakerName, "_", videoName, ".phn"])
            print phonemePath
            writeToTxt(phonemes,phonemePath)
            # i+=1

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


