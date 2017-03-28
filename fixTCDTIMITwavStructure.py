from utils.copyFilesOfType import *
from tqdm import tqdm

# we have: /home/matthijs/TCDTIMIT/TCDTIMITaudio/processed/lipspeakers/Lipspkr1/Clips/straightcam/sa1.wav
# we want: /home/matthijs/TCDTIMIT/TCDTIMITaudio/processed/lipspeakers/Lipspkr1/sa1/sa1.wav

def fixTCDTIMITwavStructure(dir, extension=".wav", interactive=False):
    src = []
    dest = []
    for root, dirs, files in os.walk(dir):

        for file_ in files:
            if file_.endswith(extension):
                srcPath = os.path.join(root, file_)
                destPath = getFixedPath(srcPath, dir)

                # after copying from source,
                # we'll have this: lipspeakers/Lipspkr1/Clips/straightcam/si1367.wav (depth 4)
                # we want this:    lipspeakers/Lipspkr1/si1367/si1367.wav            (depth 3)
                relSrcPath = relpath(dir, srcPath).lstrip("../")
                try: assert getDepth(relSrcPath) == 4  # if this doesn't work, we've already processed the file
                except: print("You probably already ran this, then the files should already be stored correctly"); continue

                print("moving from : %s \t to \t %s" % (srcPath, destPath))
                src.append(srcPath)
                dest.append(destPath)

    if len(src)>1: print("Example: copying ", src[0], "to:", dest[0])

    print(len(src), " files will be copied in total")

    if (interactive and (not query_yes_no("Are you sure you want to peform these operations?", "yes"))):
        print("Not doing a thing.")
    else:
        for i in tqdm(range(len(src))):
            if (not os.path.exists(os.path.dirname(dest[i]))):
                os.makedirs(os.path.dirname(dest[i]))
            shutil.move(src[i], dest[i])

        # remove src dirs "Clips/straightcam"
        for i in range(len(src)):
            dirToRemove = os.path.dirname(os.path.dirname(src[i]))
            assert os.path.basename(dirToRemove) == "Clips"
            if os.path.exists(dirToRemove):
                shutil.rmtree(dirToRemove)
        print("Done.")

    return 0


# input: /home/matthijs/TCDTIMIT/TCDTIMITaudio/processed/lipspeakers/Lipspkr1/Clips/straightcam/sa1.wav
#     and: /home/matthijs/TCDTIMIT/TCDTIMITaudio/processed
# output: /home/matthijs/TCDTIMIT/TCDTIMITaudio/processed/lipspeakers/Lipspkr1/sa1/sa1.wav
def getFixedPath(wrongPath, dir):
    wrongPath = os.path.abspath(wrongPath)
    file = os.path.basename(wrongPath)
    dirName = os.path.splitext(file)[0]
    fixedRelPath = os.path.dirname(os.path.dirname(os.path.dirname(wrongPath))) + os.sep + dirName + os.sep + file
    return fixedRelPath


def getDepth(relPath):
    level =relPath.count(os.sep)
    return level

# getFixedPath("/home/matthijs/TCDTIMIT/TCDTIMITaudio/processed/lipspeakers/Lipspkr1/Clips/straightcam/si1367.wav", "/home/matthijs/TCDTIMIT/TCDTIMITaudio/processed/")

if __name__ == '__main__':
    if __name__ == '__main__':
        dir = sys.argv[1]
        extension = sys.argv[2]
        fixTCDTIMITwavStructure(dir, extension=".wav", interactive=True)

