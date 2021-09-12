from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)

colorR = 255, 0, 255

cx, cy, w, h = 800, 100, 200, 200

class Rect():

    def __init__(self, center, size=[200, 200], color=[255, 0, 255]):
        self.center = center
        self.size = size
        self.color=color

    def update(self, cursor):

        oldSize = self.size
        oldColor = self.color

        cx, cy = self.center
        w, h = self.size
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.center = cursor
            self.color = [0, 255, 0]
            self.size = [220, 220]
        else:
            self.size = oldSize
            self.color = oldColor




    def setView(self, newColor=[255, 0, 255], newSize = [200, 200]):
        self.color = newColor
        self.size = newSize



rect = Rect([150, 150], [200, 200], colorR)

listOfRects = []
for x in range(5):
    listOfRects.append(Rect([x * 250 + 150, 150], [200, 200], colorR))


while True:
    # Get image frame
    success, img = cap.read()
    img = cv2.flip(img,1)
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points

        length, _, _ = detector.findDistance(lmList1[8], lmList1[12], img)

        if length <= 40:
            cursor = lmList1[8]
            for r in listOfRects:
                r.update(cursor)

        # else:
        #     for r in listOfRects:
        #         r.setView()
        #     # rect.setView()



    for r in listOfRects:
        cx, cy = r.center
        w, h = r.size
        colorR = r.color
        cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)

    # cx, cy = rect.center
    # w, h = rect.size
    # colorR = rect.color
    # cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)


    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)

