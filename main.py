import cv2
import mediapipe as mp
import time
import math
import numpy as np





def aciBulma(resim , nokta1 , nokta2 , nokta3 , liste , goster = True):

	x1 , y1 = liste[nokta1][1:]
	x2 , y2 = liste[nokta2][1:]
	x3 , y3 = liste[nokta3][1:]

	aci = math.degrees(math.atan2(y3-y2 , x3 - x2) - math.atan2(y1 - y2 , x1 - x2))

	if aci < 0:

		aci += 360

	if goster:

		cv2.line(resim , (x1 , y1) , (x2 , y2) , (255,0,0) , 3)
		cv2.line(resim , (x3 , y3) , (x2 , y2) , (255,0,0) , 3)

		cv2.circle(resim , (x1 , y1) , 10 , (0,0,255) , cv2.FILLED)
		cv2.circle(resim , (x2 , y2) , 10 , (0,0,255) , cv2.FILLED)
		cv2.circle(resim , (x3 , y3) , 10 , (0,0,255) , cv2.FILLED)

		cv2.circle(resim , (x1 , y1) , 15 , (0,0,255))
		cv2.circle(resim , (x2 , y2) , 15 , (0,0,255))
		cv2.circle(resim , (x3 , y3) , 15 , (0,0,255))

		cv2.putText(resim , str(int(aci)) , (x2 - 40 , y2 + 40) , cv2.FONT_HERSHEY_PLAIN , 2 , (0,0,255) , 2)

	return aci

poz_nesne = mp.solutions.pose
poz = poz_nesne.Pose()
cizgi = mp.solutions.drawing_utils
cap = cv2.VideoCapture("video1.mp4")
sonzaman = 0
sayi1 = 0
sayi2 = 0

while True:
	ret , frame = cap.read()
	resimRGB = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
	sonuc = poz.process(resimRGB)
	
	liste = []

	if sonuc.pose_landmarks:
		#cizgi.draw_landmarks(frame , sonuc.pose_landmarks , poz_nesne.POSE_CONNECTIONS)
		for id,i in enumerate(sonuc.pose_landmarks.landmark):
			h , w , _ = frame.shape
			cx,cy = int(i.x*w) , int(i.y*h)

			liste.append([id,cx,cy])

	if len(liste) != 0:

		aci = aciBulma(frame , 11 , 13 , 15 , liste) #11,13,15  #23,25,27
		#print(aci)

		hareket_acisi = np.interp(aci , (185 , 245) , (0,100)) #video1 185,245  #sinav65,145  #ip 120,145  #kosma200,250

		if hareket_acisi == 100:

			if sayi1 == 0:

				sayi2 += 0.5
				sayi1 = 1

		if hareket_acisi == 0:

			if sayi1 == 1:
				sayi2 += 0.5
				sayi1 = 0

		print(sayi2)

		cv2.putText(frame , str(sayi2) , (45 , 225) , cv2.FONT_HERSHEY_PLAIN , 7 , (0,255,0) , 7)



	ilkzaman = time.time()
	fps = 1/(ilkzaman - sonzaman)
	sonzaman = ilkzaman
	cv2.putText(frame,"FPS : " +str(int(fps)) , (10,60) , cv2.FONT_HERSHEY_PLAIN , 2 , (255,0,0) , 2)
			


	cv2.imshow("video",frame)

	if cv2.waitKey(1) & 0XFF == ord("q"):
		break
cv2.destroyAllWindows()
	
