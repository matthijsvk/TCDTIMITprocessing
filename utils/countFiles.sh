#!/bin/bash
#MIT License
#
#Copyright (c) 2016 matthijs van keirsbilck
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

# use this to find the number of files in directories (go through the whole tree, but only show the top level directories)
# https://forum.xfce.org/viewtopic.php?id=9106

# count nb of files per directory, print nbFiles and dirName, sort on nbFiles
files=`find . -maxdepth 1 -type d -print0 | while read -d '' -r dir; do num=$(find $dir -ls | wc -l); printf "%5d files in directory %s\n\r" "$num" "$dir"; done | perl -lane 'print "$F[0] $F[-1]\r\n"' | sort -nrk 1`

# show the number of files and the dirname in a pop-up box
echo "$files" | zenity --text-info

# print only last column (the dir name), sav to text file
echo "$files" | perl -lane 'print "$F[-1]"' > dirToRemove.txt

# now, modify text file so that it only contains the folders to remove

# then remove the folders
#cat dirToRemove.txt | xargs -d \\n rm -r




