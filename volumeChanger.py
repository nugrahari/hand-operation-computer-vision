import mediapipe as mp
import time
from scipy.spatial import distance
import alsaaudio


import cv2
# font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(0)
m = alsaaudio.Mixer()
current_volume = m.getvolume()

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
					  max_num_hands=1,
					  min_detection_confidence=0.7,
					  min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0


while True:
	cTime = time.time()
	start_point, end_point = None, None
	success, img = cap.read()
	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	results = hands.process(imgRGB)
	# print(results.multi_hand_landmarks)
	numberOfFinger = 0
	if results.multi_hand_landmarks:
		for handLms in results.multi_hand_landmarks:
			mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

			numberOfFinger += 1
			for id, lm in enumerate(handLms.landmark):
				# print(id,lm)
				h, w, c = img.shape
				cx, cy = int(lm.x *w), int(lm.y*h)
				# print(start_point, end_point)
				if(start_point is None or end_point is None):
					if id==4:
						cv2.circle(img, (cx,cy), 3, (255,0,0), cv2.FILLED)
						start_point = (cx,cy)
					elif id==8:
						cv2.circle(img, (cx,cy), 3, (255,0,0), cv2.FILLED)
						end_point = (cx,cy)
					else:
						cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)

				if(start_point is not None and end_point is not None):					
					img = cv2.line(img, start_point, end_point, (255,255,0), 3)
					dist = distance.euclidean(start_point, end_point)

					rasio_volume = 200
					if dist > rasio_volume:
						dist = rasio_volume

					volume = int((dist/rasio_volume)*100)
					# print(volume)
					try:
						current_volume = m.getvolume() # Get the current Volume
						m.setvolume(volume)
					except Exception as e:
						print(e)


	cv2.rectangle(img,(5,420),(500,460),(0,255,0),-1)

	# print(current_volume[0])
	VolumeText = F"Volume : {current_volume[0]}"
	cv2.putText(img, VolumeText, (10,450), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
	
	initialVolumePointBar = 230
	cv2.rectangle(img,(initialVolumePointBar,430),(initialVolumePointBar+current_volume[0]*2,450),(255,0,0),-1)


					

	# print(numberOfFinger)
	
	fps = 1/(cTime-pTime)
	pTime = cTime

	cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

	cv2.imshow("Image", img)
	cv2.waitKey(1)