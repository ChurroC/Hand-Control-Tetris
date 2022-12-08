import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, static_image_mode=False, max_hands=2, model_complexity=1, detection_con=0.5, track_con=0.5):
        self.static_image_mode = static_image_mode
        self.max_hands = max_hands
        self.model_complexity = model_complexity
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            self.static_image_mode, self.max_hands, self.model_complexity, self.detection_con, self.track_con)
        self.mp_draw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img, handLms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            for myHand in self.results.multi_hand_landmarks:
                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmlist.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
        return lmlist


if __name__ == "__main__":
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)
        if len(lmlist) != 0:
            print(lmlist[12])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        img = cv2.flip(img, 1)
        cv2.putText(img, str(int(fps)), (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
