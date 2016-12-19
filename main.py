# MIT License
#
# Copyright (c) 2016 matthijs van keirsbilck
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from processDatabase import *

# get phone list from file, extract phonemes and times, get the frames corresponding to those phonemes
# then remove frames without phonemes, extract faces, extract mouths, convert them to grayscale images
# also store compressed (eg 120x120) versions of grayscale faces and mouths

###################################################################################################
# !!!! Before running this, make sure all the paths to the videos in the MLF file are correct !!!!#0
###################################################################################################
startTime = time.clock()

processDatabase('./MLFfiles/volunteer_labelfiles.mlf',os.path.expanduser("~/TCDTIMIT/extracted"), 4) #storeDir requires TCDTIMIT in the name
# processDatabase('/home/user/TCDTIMIT_test/test.mlf',os.path.expanduser("~/TCDTIMIT_test/processed"), 4) #storeDir requires TCDTIMIT in the name

duration = time.clock() - startTime
print("This took ", duration, " seconds")





