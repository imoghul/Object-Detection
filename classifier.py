from objects import *
from utils import *
def getInterests(boxes):
    interests = []
    for b in boxes.copy():
        if b.Region.getClassification()=="OK": 
            interests.append(b)
    return interests
def getProposedPoles(interests):
    proposedPoles = [x for x in interests if x.Region.proposedType=="taller"]
    res = getClustersRects(proposedPoles)
    for r in res:
        r.Region = Region()
        r.Region.width = r.w
        r.Region.height = r.h
        r.Region.getProposedType()
    res.sort(key = lambda x: x.area,reverse=True)
    res = res[0:min(2,len(res))]
    return res
def getProposedTops(interests, proposedPoles):
    if proposedPoles==[]:return []
    proposedTops=[]
    midPoints = [x.midPoint for x in proposedPoles]
    lowestX = min([x[0] for x in midPoints]) 
    largestX = max([x[0] for x in midPoints])
    for i in [x for x in interests if x.Region.proposedType=="wider"]:
        if False not in[i.midPoint[1]<x[1] and i.midPoint[0]>lowestX and i.midPoint[0]<largestX for x in midPoints]: proposedTops.append(i)
    return proposedTops