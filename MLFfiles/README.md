- See lispeaker_labelfiles.mlf and volunteer_labelfiles.mlf.  
- They are structured as follows:  
    1. path to a video file.  
    2. on each line: `startTime <space> endTime <space> phoneme`  
    3. `.`to signify the end of a video file  

- You can extract phoneme files per video using extractTCDTIMITaudio. It can also copy the wav files.  You can then fix the headers and replace the phonemes by [audioSR](https://github.com/matthijsvk/multimodalSR/tree/master/code/audioSR)/transform.py

- These labelfiles have been modified slightly from the original TCDTIMIT files:  
    1. the path of the videos has to be replaced by wherever you've downloaded and extracted TCDTIMIT (see `downloadTCDTIMIT` for a script to do that)  
    1. in a few videos, a phoneme was repeated twice after eachother. It should be one interval until the next (different) phoneme starts