import numpy as np
import cv2
from objects import *
# stacks multiple images into 1 frame
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def boudingBoxRegions(regions):
    lefts=[i.left for i in regions]
    rights=[i.right for i in regions]
    ups=[i.up for i in regions]
    downs=[i.down for i in regions]
    left=int(min(lefts))
    right=int(max(rights))
    up=int(min(ups))
    down=int(max(downs))
    return Rect(left,up,right-left,down-up)

def conflictsRemainRegion(l):
        for group in range(len(l)):
            for rect in range(len(l)):
                    for r in range(len(l)):
                        #print(l[group][rect].getNum() , ((l[group][rect].isIn(l[g][r]) or l[group][rect].getTooClose(l[g][r])) and (group==g and rect==r)))
                        if(((l[rect].isIn(l[r]) and not(rect==r)))):#not(l[group][rect].isEqual(l[g][r])))):
                            return True
        return False;
def getClustersRegions(rects):
    if(conflictsRemainRegion(rects)):
        for rect in range(len(rects)):
            for other in range(len(rects)):
                if(not(rect==other)) and rects[rect].isIn(rects[other]):
                    bounding = boudingBoxRegions([rects[rect],rects[other]])
                    a = rects[rect]
                    b = rects[other]
                    rects.remove(a)
                    rects.remove(b)
                    rects.append(bounding)
                    return getClustersRegions(rects)

    else:
        rects.sort(key=lambda target:target.getArea())
        rects.reverse()
        return rects[0:2]


def boundingBoxRects(rectangles,n=None):
    minX=[]
    minY=[]
    maxX=[]
    maxY=[]
    if(type(rectangles)==Rect):
        rectangles=[rectangles]
    if(not rectangles==None and len(rectangles)>0):
        for r in rectangles:
            minX.append(r.getX())
            maxX.append(r.getX()+r.getW())
            minY.append(r.getY())
            maxY.append(r.getY()+r.getH())
        r = Rect(min(minX),min(minY),max(maxX)-min(minX),max(maxY)-min(minY),n)
        return r
# the condition on which 2 boxes will combine
def isConflictingRect(l, index1,index2):
    return (not(index1==index2)) and ((l[index1].isIn(l[index2]) or l[index1].getTooClose(l[index2])))
# returns if there are still any conflicts remaining
def conflictsRemainRect(l):
        for group in range(len(l)):
            for rect in range(len(l)):
                    for r in range(len(l)):
                        if(isConflictingRect(l,rect,r)):
                            return True
        return False;
# recursively combines rects until a big supposed object is created
def getClustersRects(rectangles):
    rects = rectangles.copy()
    if(conflictsRemainRect(rects)):
        for rect in range(len(rects)):
            for other in range(len(rects)):
                if(isConflictingRect(rects,rect,other)):
                    bounding = boundingBoxRects([rects[rect],rects[other]])
                    a = rects[rect]
                    b = rects[other]
                    rects.remove(a)
                    rects.remove(b)
                    rects.append(bounding)
                    return getClustersRects(rects)

    else:
        rects.sort(key=lambda target:target.getArea())
        rects.reverse()
        return rects
