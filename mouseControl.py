import cv2
# import pyautogui
import mouse
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
					  max_num_hands=1,
					  min_detection_confidence=0.7,
					  min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

current_coordinate = None
while True:
	success, img = cap.read()
	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	results = hands.process(imgRGB)
	# print(results.multi_hand_landmarks)
	numberOfFinger = 0
	if results.multi_hand_landmarks:
		for handLms in results.multi_hand_landmarks:
			numberOfFinger += 1
			mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
			for id, lm in enumerate(handLms.landmark):
				# print(id,lm)
				h, w, c = img.shape
				cx, cy = int(lm.x *w), int(lm.y*h)
				
				if id==8:
					cv2.circle(img, (cx,cy), 8, (255,0,0), cv2.FILLED)
					# end_point = (cx,cy)
				
				if current_coordinate is None:
					current_coordinate = [cx,cy]
				else:
					# move_coordinate = tuple(map(lambda i, j: i - j, current_coordinate, (cx,cy))) 
					move_x = current_coordinate[0] - cx 
					move_y = current_coordinate[1] - cy
					current_coordinate = [cx,cy]
					# pyautogui.moveRel(move_x, move_y) 
					# print(move_x, move_y)
					# mouse.drag(current_coordinate[0], current_coordinate[1], cx, cy,True,0)
					mouse.drag(0, 0, move_x, move_y*-1,False,0)
	else:
		current_coordinate = None

	# print(numberOfFinger)
	cTime = time.time()
	fps = 1/(cTime-pTime)
	pTime = cTime

	cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

	cv2.imshow("Image", img)
	cv2.waitKey(1)