import time

relPath = "test/dir/dir2/volunteers/Lipspkr1/sa1/sa1.phn"
topDir = relPath.split('/')[0]
print topDir
while not (topDir == "volunteers" or topDir == "lipspeakers"):
    relPath = '/'.join(relPath.split('/')[1:])
    topDir = relPath.split('/')[0]

    print relPath, topDir
    time.sleep(0.5)
print relPath