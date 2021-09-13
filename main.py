from cvzone.HandTrackingModule import HandDetector
import cv2
import cvzone
import numpy as np

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)

colorR = 255, 0, 255

cx, cy, w, h = 800, 100, 200, 200
startDist = None
scale = 0

class Rect():

    def __init__(self, center, size=[200, 200], color=[255, 0, 255], isResizing=False):
        self.center = center
        self.size = size
        self.color = color
        self.isResizing = isResizing

    def update(self, cursor):
        cx, cy = self.center
        w, h = self.size
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.center = cursor
            self.color = [0, 255, 0]





    def between(self,info):
        w, h = self.size
        cx, cy = self.center
        if cx - w // 2 < info[0] < cx + w // 2 and cy - h // 2 < info[1] < cy + h // 2:
            self.isResizing = True
            self.center = info
        else:
            self.isResizing = False

    def leftBetween(self):
        self.isResizing = False

    def updateSize(self,scale):
        w, h = self.size
        if self.isResizing:
            h = h + scale
            w = w + scale
        return [w, h]





listOfRects = []
for x in range(5):
    listOfRects.append(Rect([x * 250 + 150, 150], [200, 200], colorR))


while True:
    # Get image frame
    success, img = cap.read()
    img = cv2.flip(img,1)
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw

    if len(hands) == 1:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points

        length, _, _ = detector.findDistance(lmList1[8], lmList1[12], img)

        if length <= 40:
            cursor = lmList1[8]
            for r in listOfRects:
                r.update(cursor)



    elif len(hands) == 2:
        hand1 = hands[0]
        hand2 = hands[1]

        if detector.fingersUp(hand1) == [1, 1, 0, 0, 0] and detector.fingersUp(hand2) == [1, 1, 0, 0, 0]:
            lmList1 = hand1["lmList"]  # List of 21 Landmark points
            lmList2 = hand2["lmList"]  # List of 21 Landmark points

            length, info, img = detector.findDistance(lmList1[5], lmList2[5], img)


            if startDist is None:
                startDist = length
            length, info, img = detector.findDistance(lmList1[5], lmList2[5], img)
            scale = int((length - startDist)//2)
            for r in listOfRects:
                r.between(info[4:])
            # info stores x, y center points
            cx = info[4]
            cy = info[5]
            print(info)

    else:
        startDist = None
        for r in listOfRects:
            r.leftBetween()




    #Draw transparent rect
    imgNew = np.zeros_like(img, np.uint8)
    for r in listOfRects:
        cx, cy = r.center
        w, h = r.size

        newWidth, newHeight = r.updateSize(scale)


        colorR = r.color
        cv2.rectangle(imgNew, (cx - newWidth // 2, cy - newHeight // 2), (cx + newWidth // 2, cy + newHeight // 2), colorR, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    out = img.copy()
    alpha = 0.1
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img,alpha,imgNew,1-alpha,0)[mask]


    # Display
    cv2.imshow("Image", out)
    cv2.waitKey(1)

