from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)
colorR = 255, 0, 255

cx, cy, w, h = 800, 100, 200, 200


while True:
    # Get image frame
    success, img = cap.read()
    img = cv2.flip(img,1)
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw

    cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED)

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points


        l, _, _ = detector.findDistance(lmList1[8], lmList1[12], img)

        if l <= 35:
            cursor = lmList1[8]
            if cx-w//2 < cursor[0] < cx + w//2 and cy-h//2 < cursor[1] < cy+h//2 :
                colorR = 0, 255, 0
                cx, cy = cursor
        else:
            colorR = 255, 0, 255




    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)

