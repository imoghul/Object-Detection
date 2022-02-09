import cv2 as cv
from cv2 import boundingRect
import imutils
import ObjectDetection
import numpy as np
import random
import argparse
from utils import *
import time
from objects import *
from classifier import *

print("q: to quit")#\nt: to toggle automatically detecting when there is action(current state shown by color of border)\nd: to force a detection unconditionally")

### this section determines what file to analyze
file = ""

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image",required=False,help="path to input image")
ap.add_argument("-v", "--video",required=False,help="path to input video")
args = vars(ap.parse_args())
image = (args["image"])
video = (args["video"])
isVideo = not video == None
if(isVideo):
    file=video
    if(video.isnumeric()):
        video = int(video)
        file="webcam"
else:
    file=image

if(isVideo):
    webcam = cv.VideoCapture(video)
    webcam.read()
###

### creating trackbars for tuning
def empty(a):
    pass

cv.namedWindow("Final")

cv.createTrackbar("Threshold1","Final",15,255,empty)#30
cv.createTrackbar("Threshold2","Final",100,255,empty)#10
# cv.createTrackbar("Sigma","Final",12,100,empty)#10



###
global fps
detectedObjects=[]
detected=None
fps = 60
isClassifying=False # if automatic contour detection to neural network detection is on
key=cv.waitKey(1)
lastTime = int(time.time())
prevFrame = None
while(not (key & 0xFF == ord('q'))): # main loop
    timer = cv.getTickCount()
    key=cv.waitKey(1)

    randColor=(random.randint(0,256),random.randint(0,256),random.randint(0,256))

    if(isVideo):
        ret, frame = webcam.read()
    else:
        frame=cv.imread(image)
    if(not(type(frame)==np.ndarray)):
        print("\n    finished\n")
        break;

    # frame = frame[:,:,0]
    real = imutils.resize(frame,width=750) # resizes the image (WIDTH MUST BE 750 OTHERWISE ALL OTHER MAGIC NUMBERS WON'T WORK)
    originalFrame = real.copy() # a copy of the original frame
    frame = real#cv.GaussianBlur(imutils.resize(imutils.resize(imutils.resize(real,width=1000),width=100),width=750),(11,11),0)
    ### processes image and get objects
    thresh1 = cv.getTrackbarPos("Threshold1", "Final")# if fps>20 else 255
    thresh2 = cv.getTrackbarPos("Threshold2", "Final")# if fps>20 else 255
    processed = ObjectDetection.getProcessed(frame,threshold1=thresh1,threshold2=thresh2)
    contours = ObjectDetection.getContours(processed)
    targets = ObjectDetection.getTargets(contours)
    boxes = targets#ObjectDetection.getBoxes(targets)
    objects = ObjectDetection.getObjects(boxes)#ObjectDetection.getObjectsFinal(frame, threshval1 = thresh1, threshval2 = thresh2)
    ### image initialization for each frame
    empty = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
    blank = empty.copy()
    screen = empty.copy()
    targetFrame = empty.copy()
    if(type(detected)==type(None)):
        detected=empty.copy()
    # draw contours
    cv.drawContours(blank, contours, -1, (255, 255, 255), 1)
    # draw targets
    for t in targets:
        t.drawColor(processed,(255,0,0),thickness=1)
        cat = t.Region.getClassification()
        if cat!="BAD": t.Region.drawColor(blank,(0,255,0),thickness=1)
        else : t.Region.drawColor(blank,(0,0,255),thickness=1)
    for b in boxes:
        b.drawColor(processed,(0,255,0),thickness=1)
    # gate detection
    interests = getInterests(boxes)
    proposedPoles = getProposedPoles(interests)
    proposedTops = getProposedTops(interests,proposedPoles)
    gateBoxes = proposedPoles+proposedTops
    gateBox = boundingBoxRects(gateBoxes)
    for i in proposedPoles:
        i.drawColor(screen,(255,100,0),thickness=1)
    for i in proposedTops:
        i.drawColor(screen,(100,255,0),thickness=1)
    if gateBox!=None:
        gateBox.Region = Region()
        gateBox.Region.width = gateBox.w
        gateBox.Region.height = gateBox.h
        if gateBox.Region.getProposedType()=="wider":gateBox.drawColor(frame,(0,0,255))
    # stitching images and writing output
    stacked = stackImages(1,([blank,processed],[screen,frame]))
    fps = cv.getTickFrequency() / (cv.getTickCount() - timer)
    cv.putText(stacked,file + " fps: "+str(int(fps)), (75, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (20,230,20) if fps>60 else ((230,20,20) if fps>20 else (20,20,230)), 2)
    stacked = imutils.resize(stacked,height=800)#cv.resize(stacked,(1200,850))
    cv.imshow("Final",stacked)
if(isVideo):
    webcam.release()
cv.destroyAllWindows()

