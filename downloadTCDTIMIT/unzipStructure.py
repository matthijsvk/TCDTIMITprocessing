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

import zipfile, os.path
import concurrent.futures
import threading

from helpFunctions import *
import os, errno
import subprocess

# Some helper functions
def silentremove (filename):
    try:
        os.remove(filename)
    except OSError as e:  # name the Exception `e`
        pass #print("Failed with:", e.strerror)  # look what it says
    return 0

# create a list with paths of all zip files
def createZipList(rootDir):
    zipList= []
    for root, dirs, files in os.walk(rootDir):
        for fname in files:
            if ".zip" in fname:
                path = ''.join([root, os.sep, fname])
                #print('Found zip: %s' % path)
                zipList.append(path)
    return zipList

# define func to unzip one file
import zipfile
def extractZip(filePath, delete=False):
    targetDir = os.path.dirname(filePath)
    with zipfile.ZipFile(filePath, "r") as z:
        z.extractall(targetDir)
    if (delete):
        silentremove(filePath)
    return 0

######################################
########## Main Function #############
######################################

rootDir = "/media/matthijs/TOSHIBA EXT/TCDTIMIT/volunteers"
batchSize = 1 # 1 or 2 recommended

zipList= createZipList(rootDir)
print("\n".join(zipList))

if query_yes_no("Would you like to process these zip files?", "yes"):
    deleteZips = query_yes_no("Would you like to remove the zip files after extraction?", "no")
    batchIndex = 0
    executor = concurrent.futures.ProcessPoolExecutor(batchSize)
    running = 1
    while running:
        # get commands for current batch
        if batchIndex + batchSize > len(zipList):
            print("Processing LAST BATCH...")
            running = 0
            currentZips = zipList[batchIndex:]  # till the end
        else:
            currentZips = zipList[batchIndex:batchIndex + batchSize]

        # execute the commands
        futures = []
        for i in range(len(currentZips)):
            filePath = currentZips[i]
            print("Unzipping ", filePath)
            futures.append(executor.submit(extractZip, filePath, deleteZips))
        concurrent.futures.wait(futures)

        # update the batchIndex
        batchIndex += batchSize

        print "One batch complete."
        print "---------------------------------"

    print "All done!"
else:
    print("Okay, then goodbye!")





